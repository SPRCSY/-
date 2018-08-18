#encoding:utf-8
from api.wallet import WalletClient
from rest.api.api import Client
import json
import os
import requests

apikey = "i06tyGPHM1533007579"
cert_path = "/usr/local/lib/python2.7/dist-packages/py_common-2.0.1-py2.7.egg/cryption/ecc/certs"
ip_addr = "http://139.198.15.132:9143"
ent_sign_param = {
     "creator": "did:axn:a010d9e9-3c70-4b57-bbc2-b947f762da2d",
     "created": "LMIumn3AvQoHZHL4dxWw2DHv",
     "nonce": "nonce",
     "privateB64": "bZnw/gJ63EPho9D+ts51Dakx+aYr3F8SLfeACVY6qLh7vxVEm46zvYTBfwo5Du0vu6mCVd9v0Q/EB+j7TuR0yA=="
 }
client = Client(apikey, cert_path, ent_sign_param, ip_addr)
walletclient = WalletClient(client)
header = {"Bc-Invoke-Mode": "sync"}

def Err(p):
    print "失败,原因是",p["ErrMessage"],"错误码：",p["ErrCode"]

def register():
    body = {
        "id":raw_input("请输入您的身份证号码:"),
        "access":raw_input("请设置您的用户名4-36位"),
        "phone":raw_input("(可选) 设置用户手机号："),
        "email":raw_input("(可选) 设置用户Email："),
        "secret":raw_input("请设置您的登录密码(由8-16位英文大小写字母和数字组成，必须同时包含大小写字母和数字)：\n"), # 普通用户密码, 由8-16位英文大小写字母和数字组成，必须同时包含大小写字母和数字
        "type":raw_input("请输入您的用户类型(Organization/Person/Dependent/Independent)：\n"), # 类型
            } 
    _,r = walletclient.register(header,body)
    print "您的信息为\n",r
    with open('wallet_did.json',"w") as f:
        json.dump(r,f)
    print "请妥善保管您的用户名、密码、id和did\n"

def login():
    print "登录"
    access=raw_input("用户名：")
    secret=raw_input("密  码：")
    did=raw_input("钱包did：")
    body={"credential": {"value": {"access": access, "secret": secret}}}
    r = requests.post("http://139.198.15.132:9143/fred/v1/auth/token", json=body)
    p=json.loads(r.text)
    if p["ErrCode"] != 0:
        Err(p)
        login()
    else:
        print "登录成功，信息为：",p
        with open('login.json','wb') as f:
            f.write(r.text)
        return p["token"]["value"],did  

def query_block_detials(XAuthToken):
    print "查询区块详情"
    n=raw_input("输入区块编号：")
    headers={'X-Auth-Token' : XAuthToken}
    r=requests.get(ip_addr+"/chain-monitor/v1/chain/block_detail?height="+n, headers=headers)
    print "查询结果:\n",r.text

def query_transaction_details():
    print "查询交易详情"
    transaction_id = raw_input("输入交易id：")
    _, resp = walletclient.query_txn_logs_with_id({"Bc-Invoke-Mode":"sync"}, type_="" ,id_=transaction_id,) # 交易ID
    print resp.text

def create_poe():
     print "unfinished"

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
XAuthToken,DID = login()
XAuthToken = json.load(login)["token"]["value"]
main()
