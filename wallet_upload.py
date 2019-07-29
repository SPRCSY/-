#encoding:utf-8

from rest.api.api import Client
import json
import csv
import os
import requests
import time
from wallet_init import WalletInit

class WalletUpload(WalletInit):
    def __init__(self, ):
        WalletInit.__init__(self)
    
    #创建数字存证并上传存证文件
    def create_poe(self,json_metadata,FileName,PoeName):
        with open("cache/login_temp.json","rb") as f:
            q = json.load(f)
        self.walletinit = WalletInit()
        self.did = q["did"]
        with open('api_data.csv','rb',encoding='utf-8') as f:
            reader= csv.DictReader(f)
            js = dict(reader)        
        payload = {
            "id": "", # 若传的数字存证id是空，则系统会自动生成
            "name": PoeName, # poe name
            "hash": "",
            "parent_id": "",
            "owner": self.did, # 企业用户钱包DID，如：did:axn:***2fc68-f51e-4aff-b6e4-427cce3ed1af
            "metadata": [ord(x) for x in json.dumps(json_metadata)] # metadata的数据格式是byte数组，需要将json格式的数据进行处理, 如 [ord(x) for x in json.dumps(json格式的metadata数据)]
        }
            #"metadata": map(ord, '{"address": "xxx", "telephone": "xxx", ...}'
        params = {
            "creator": self.did, # 企业用户钱包DID，如：did:axn:***2fc68-f51e-4aff-b6e4-427cce3ed1af
            "created": str(int(time.time())),
            "nonce": "nonce", # your nonce for ed25519 signture
            "privateB64": js["privateB64"], # 企业用户交易签名凭证，如：***+oEuaelf2aecUZvG7xrWr+p43ZfjGZYfDCXfQD+ku0xY5BXP8kIKhiqzKRvfyKBKM3y7V9O1bF7X3M9mxkQ==
            "payload": payload
        }
        _, response = self.walletclient.create_poe(self.header, payload, params)
        with open('PoeList/poeid'+json.loads(response)["payload"]["id\\"]+'.json','wb') as f:
            f.write(response)
        self.__poeid = json.loads(response)["payload"]["id\\"]
        self.__FileName = FileName
        self.__readonly = "False"
        _, self.__response = self.walletclient.upload_poe({}, self.__FileName, self.__poeid, self.__readonly)
        return self.__response
        
'''
        #上传存证文件
        def UploadPoeFile(self,FileName,PoePath):
            self.__PoePath = PoePath
            self.__FileName = FileName
            with open(self.__PoePath ,'rb') as f:
                self.__reader = json.load(f)
            #filename = "file path"
            self.__poeid = self.__reader["payload"]["id\\"]
            self.__readonly = "False"
            _, self.response = self.wallet.upload_poe({}, self.__FileName, self.__poeid, self.__readonly)
            return self.response
'''

