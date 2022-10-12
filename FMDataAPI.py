import requests
import urllib.parse
import json
import time
import datetime
import os.path
import base64
# print(base64.b64encode('こんにちは'.encode()))

class FMDataAPI():

    def __init__(self, *args, **kwargs):
        self.RMDataAPILogin()

    def RMDataAPILogin(self):

        path = os.path.expanduser('~/init2.json')
        f = open(path, 'r')
        datajson = json.loads(f.read())
        f.close()
        self.serverAddress = "192.168.0.171"
        self.databaseName = "楽楽明細"
        self.layoutName = "顧客リスト"
        # RecId = 125
        self.URL1 = datajson['URL1']
        self.URL2 = datajson['URL2']
        self.URL3 = datajson['URL3']

        URL = self.URL1.format(self.serverAddress, self.databaseName)

        self.USER = datajson['USER']
        self.PASSWORD = datajson['PASSWORD']
        self.idpw = base64.b64encode((self.USER + ':' + self.PASSWORD).encode()).decode()
 
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.idpw
            }
        
       # POST送信
        response = requests.post(
            URL,
            headers=headers,
            json = {},
            verify=False
        )

        if response.status_code==200:
            res = response.text
            json_dict = json.loads(res)
            self.access_token = json_dict['response']['token']
            self.settime = datetime.datetime.now()
        else:
            res = ""
            self.access_token = ""
            
    def RMDataAPILogOut(self):

        URL = self.URL1.format(self.serverAddress, self.databaseName) + '/' + self.access_token
 
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.idpw
            }
        
       # POST送信
        response = requests.delete(
            URL,
            headers=headers,
            json = {},
            verify=False
        )
        if response.status_code==200:
            res = response.text
        else:
            res = ""
        return res

    def datareadbyID(self):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.RMDataAPILogin()
        
        url = self.URL2.format(self.serverAddress, self.databaseName, self.layoutName, 125)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + ' ' + self.access_token
        }
        
        response = requests.get(
            url,
            headers=headers,
            verify=False
        )
        if response.status_code==200:
            res = response.text
        else:
            res = ""
        return res

    def datareadbyFind(self):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.RMDataAPILogin()
        
        url = self.URL3.format(self.serverAddress, self.databaseName, self.layoutName)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + ' ' + self.access_token
        }
        
        json1 = {
            "query":[
                    {"更新日時": "04/01/2021...03/31/2023","担当部署名": "総務課" }
                    ],
            "sort": [
                    {"fieldName": "更新日時","sortOrder": "ascend" }
                    ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=json1,
            verify=False
        )
        if response.status_code==200:
            res = response.text
        else:
            res = ""
        return res

if __name__ == '__main__':
    sf = FMDataAPI()
    # print(sf.access_token)
    res1 = sf.datareadbyID()
    if res1 != "":
        # print(res1)
        json_dict = json.loads(res1)
        
        n = int(json_dict['response']['dataInfo']['returnedCount'])
        for i in range(n):
            name = json_dict['response']['data'][i]['fieldData']['顧客名']
            print(name)

    res2 = sf.datareadbyFind()
    if res2 != "":
        # print(res2)
        json_dict = json.loads(res2)
        n = int(json_dict['response']['dataInfo']['returnedCount'])
        for i in range(n):
            name = json_dict['response']['data'][i]['fieldData']['顧客名']
            print(name)

    res3 = sf.RMDataAPILogOut()
    print(res3)