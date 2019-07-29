#encoding:utf-8
import csv
import json
import os

import requests
from api.wallet import WalletClient
from rest.api.api import Client

apikey = "i06tyGPHM1533007579"
cert_path = "D:\\Python2.7\\Lib\\site-packages\\py_common-3.0-py2.7.egg\\cryption\\ecc\\certs"
ip_addr = "http://139.198.15.132:9143"
ent_sign_param = {
    "creator": "did:axn:a010d9e9-3c70-4b57-bbc2-b947f762da2d",
    "created": "LMIumn3AvQoHZHL4dxWw2DHv",
    "nonce": "nonce",
    "privateB64": "bZnw/gJ63EPho9D+ts51Dakx+aYr3F8SLfeACVY6qLh7vxVEm46zvYTBfwo5Du0vu6mCVd9v0Q/EB+j7TuR0yA=="
}

class WalletInit():
    def __init__(self,):
        #self.apikey = apikey
        #self.cert_path = cert_path
        #self.ip_addr = ip_addr
        with open('api_data.csv','rb',encoding='utf-8') as f:
            reader= csv.DictReader(f)
            js = dict(reader)
        self.apikey = js['apikey']
        self.cert_path = js['cert_path']
        self.ip_addr = js['ip_addr']
        self.__creator = js['creator']
        self.__created = js['created']
        self.__nonce = js['nonce']
        self.__privateB64 = js['privateB64']
        self.ent_sign_param = {"creator":self.__creator , "created":self.__created, "nonce":self.__nonce ,"privateB64":self.__privateB64}
        self.client = Client(self.apikey, self.cert_path, self.ent_sign_param, self.ip_addr)
        self.walletclient = WalletClient(self.client)
        self.header = {"Bc-Invoke-Mode": "sync"}

    def Err(self, p):
        self.__p = p
        print "失败,原因是",self.__p["ErrMessage"],"错误码：",self.__p["ErrCode"]

    #注册钱包
    def register(self, id_number,access, secret, usertype, save=0):
        self.__access=access
        self.__id = id_number #填身份证号码
        self.__password = secret
        self.__type = usertype #"Organization" / "Person" / "Dependent" / "Independent"
        self.__save = save
        self.__body = {
                    "id":"",
                    "access": self.__access, #钱包用户名称
                    "password":self.__password, #钱包登录口令 (由8-16位英文大小写字母和数字组成，必须同时包含大小写字母和数字)
                    "type":self.__type,#建议用复选框传字符串进来，选项在下方注释  
                    "public_key":  { #如果没有提供，则由服务自动生成
                        "usage": "", #公钥的使用用途
                        "key_type": "", #公钥的类型
                        "public_key_data": "" #钱包公钥（ED25519，Base64编码）
                    }            
        }
        
        _,r = self.walletclient.register(self.header,self.__body)
        print "您的信息为\n",r
        if(self.__save == 1):
            with open('wallet_did.txt',"wb") as f:
                json.dump(r,f) #注册完成后用户名密码和did会被存放在工作目录下一个叫wallet_did.txt的文件中
        #print "请妥善保管您的用户名、密码、id和did\n"

    def login(self, access=None , secret=None, did=None):
        self.__access=access
        self.__secret=secret
        self.__did=did
        body={"credential": {"value": {"access": access, "secret": secret}}}
        r = requests.post(ip_addr+"/fred/v1/auth/token", json=body)
        p=json.loads(r.text)
        if p["ErrCode"] == 0:
           # print "登录成功，信息为：",p
            with open('login.json','wb') as f:
                f.write(r.text)
            with open('cache/login_temp.json','wb') as f:
                json.dump(json.dumps({"access":self.__access, "secret":self.__secret, "did":self.__did}),f)
            return p["token"]["value"]
        else:
            #失败，重新登陆
            pass  

    #查询区块详情
    #XAuthToken,DID = login()
    #XAuthToken = json.load(login)["token"]["value"]
    def query_block_detials(self,XAuthToken,BlockCode):
        self.__XAuthToken = XAuthToken
        self.__BlockCode = BlockCode #传入区块编号 
        #n=raw_input("输入区块编号：")
        self.__headers={'X-Auth-Token' : self.__XAuthToken}
        r=requests.get(ip_addr+"/chain-monitor/v1/chain/block_detail?height="+self.__BlockCode, headers=self.__headers)
        return r

    #"查询交易详情"
    def query_transaction_details(self,transaction_id):
        print 
        self.__transaction_id = transaction_id #交易ID
        _, resp = self.walletclient.query_txn_logs_with_id({"Bc-Invoke-Mode":"sync"}, type_="" ,id_=transaction_id,) # 交易ID
        print resp.text

    '''
    def main():
        while(1):
            print "功能列表：(输入方括号内数字以访问对应功能）"
            print "[-1]查询区块详情\n[0]查询交易详情\n[]"
            switch = {
                "-1":query_block_detials(XAuthToken),
                "0":query_transaction_details(),
                "1":create_poe()
            }
            case = raw_input("请输入输入功能编号：")
            switch[case]

print "欢迎使用区块链医疗存证系统"
answer0=input("请问您是否已经注册？\n  未注册请扣0注册，已注册用户请扣1登录:")
if answer0 == 0:
    register()
#XAuthToken,DID = login()
#XAuthToken = json.load(login)["token"]["value"]
main()
'''
