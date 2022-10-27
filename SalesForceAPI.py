from email import header
import requests
import urllib.parse
import json
import time
import datetime
import os.path

class SalesForceAPI():

    def __init__(self, *args, **kwargs):
        self.tokenReset()

    def tokenReset(self):
    
        # init.jsonファイルからURL,ID,SECRET,USER,PASSWORDを読み込む
        path = os.path.expanduser('~/init.json')
        f = open(path, 'r')
        datajson = json.loads(f.read())
        f.close()
        URL = datajson['URL']
        ID = datajson['ID']
        SECRET = datajson['SECRET']
        USER = datajson['USER']
        PASSWORD = datajson['PASSWORD']

        data = {'client_id': ID,
                'client_secret': SECRET,
                'username': USER,
                'password': PASSWORD,
                'grant_type': 'password'
                }
        # POST送信（アクセストークンをサーバーへ申請）
        response = requests.post(
            URL,
            data=data
        )
        if response.ok:
            self.res = response.text
        # 受け取ったアクセストークンとトークンタイプを変数にセット
            json_dict = json.loads(self.res)
            self.access_token = json_dict['access_token']
            self.instance_url = json_dict['instance_url']
            self.id = json_dict['id']
            self.token_type = json_dict['token_type']
            self.issued_at = json_dict['issued_at']
            self.signature = json_dict['signature']
            self.settime = datetime.datetime.now()
            # print(self.access_token)
            self.url = ""
            self.resourse = {}
            self.loginOk = True
        else:
            self.loginOk = False

    def datareadbyQuerry(self,query):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.tokenReset()
        if self.loginOk:
            # query = 'SELECT Name__c,Address1__c,Section_Name__c,Name FROM Customer_Data1__c WHERE Name__c LIKE \'東海カラー%\''
            # url = self.instance_url + self.url + "/query/?q=" + query
            # headers = {'Authorization': self.token_type + ' ' + self.access_token}
            response = requests.get(
                self.instance_url + self.url + "/query/?q=" + query,
                headers={'Authorization': self.token_type + ' ' + self.access_token}
            )
            res = response.text
        else:
            res = ""
        return res

    def mataDataRead(self, sObject="Customer_Data1__c"):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.tokenReset()
        if self.loginOk:
            response = requests.get(
                self.instance_url + self.url + "/sobjects/" + sObject + "/",
                headers={'Authorization': self.token_type + ' ' + self.access_token}
            )
            res = response.text
        else:
            res = ""
        return res

    def version(self):
        # url = self.instance_url + "/services/data" 
        if self.loginOk:
            response = requests.get(
                self.instance_url + "/services/data",
            )
            res = response.text
        else:
            res = ""
        return res

    def getResourse(self):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.tokenReset()
        if self.loginOk:
            response = requests.get(
                self.instance_url + self.url,
                headers={'Authorization': self.token_type + ' ' + self.access_token}
            )
            res = response.text
        else:
            res = ""
        return res

    def getObjectList(self):
            if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
                self.tokenReset()
            if self.loginOk:
                response = requests.get(
                    self.instance_url + self.url + "/sobjects/",
                    headers={'Authorization': self.token_type + ' ' + self.access_token,
                    'X-PrettyPrint':'1'}
                )
                res = response.text
            else:
                res = ""
            return res

    def getLimit(self):
            if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
                self.tokenReset()
            if self.loginOk:
                response = requests.get(
                    self.instance_url + self.url + "/limits/",
                    headers={'Authorization': self.token_type + ' ' + self.access_token,
                    'X-PrettyPrint':'1'}
                )
                res = response.text
            else:
                res = ""
            return res

    def getObjecInfo(self, sObject="Customer_Data1__c"):
            if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
                self.tokenReset()
            if self.loginOk:
                response = requests.get(
                    self.instance_url + self.url + "/sobjects/" + sObject + "/",
                    headers={'Authorization': self.token_type + ' ' + self.access_token,
                    'X-PrettyPrint':'1'}
                )
                res = response.text
            else:
                res = ""
            return res


    def getFieldName(self, sObject="Customer_Data1__c"):
            if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
                self.tokenReset()
            if self.loginOk:
                response = requests.get(
                    self.instance_url + self.url + "/sobjects/" + sObject + "/describe/",
                    headers={'Authorization': self.token_type + ' ' + self.access_token,
                    'X-PrettyPrint':'1'}
                )
                res = response.text
            else:
                res = ""
            return res

if __name__ == '__main__':
    sf = SalesForceAPI()
    print(sf.access_token)

# APIのバージョンを取得
    res = sf.version()
    if res != "":
        data = json.loads(res)
        n = len(data)
        sf.url = data[n-2]["url"]   # 最新のひとつ前のバージョンを指定
        print(sf.url)

    res = sf.getResourse()
    if res != "":
        sf.resourse = json.loads(res)
        print(json.dumps(data, indent=4))

    res = sf.getObjectList()
    if res != "":
    # print(res)
        data = json.loads(res)
        print(json.dumps(data, indent=4))

    res = sf.getLimit()
    if res != "":
    # print(res)
        data = json.loads(res)
        print(json.dumps(data, indent=4))

    res = sf.getObjecInfo("Customer_Data1__c")
    if res != "":
    # print(res)
        data = json.loads(res)
        print(json.dumps(data, indent=4))

    res = sf.getFieldName("Customer_Data1__c")
    if res != "":
        # print(res)
        data = json.loads(res)
        fields = data['fields']
        objectLabel = data['label']
        name = []
        fieldType = {}
        fieldLabel = {}
        for field in fields:
            name.append(field["name"])
            fieldType[field["name"]] = field["type"]
            fieldLabel[field["name"]] = field["label"]
        print(json.dumps(field, indent=4))

    res = sf.mataDataRead("Customer_Data1__c")
    if res != "":
        # print(res)
        data = json.loads(res)
        print(json.dumps(sf.resourse, indent=4))

    query = 'SELECT Name__c,Address1__c,Section_Name__c,Name FROM Customer_Data1__c WHERE Name__c LIKE \'東海カラー%\'' 
    res = sf.datareadbyQuerry(query)
    if res != "":
        print(res)
        json_dict = json.loads(res)
        n = int(json_dict['totalSize'])
        for i in range(n):
            name = json_dict['records'][i]['Name__c']
            print(name)