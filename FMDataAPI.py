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
        self.tokenReset()

    def tokenReset(self):
        # f = open('/Users/tkanyama/マイドライブ/init.txt', 'r')
        # path = os.path.expanduser('~/init.txt')
        # f = open(path, 'r')
        # datalist = f.readlines()
        # f.close()
        # URL = datalist[0].rstrip('\n')
        # ID = datalist[1].rstrip('\n')
        # SECRET= datalist[2].rstrip('\n')
        # USER= datalist[3].rstrip('\n')
        # PASSWORD = datalist[4].rstrip('\n')

        path = os.path.expanduser('~/init2.json')
        f = open(path, 'r')
        datajson = json.loads(f.read())
        f.close()
        self.serverAddress = "192.168.0.171"
        self.databaseName = "楽楽明細"
        self.layoutName = "顧客リスト"
        RecId = 125
        self.URL1 = datajson['URL1']
        self.URL2 = datajson['URL2']
        self.URL3 = datajson['URL3']

        URL = self.URL1.format(self.serverAddress, self.databaseName)
        # ID = datajson['ID']
        # SECRET = datajson['SECRET']
        USER = datajson['USER']
        PASSWORD = datajson['PASSWORD']
        idpw = base64.b64encode((USER + ':' + PASSWORD).encode()).decode()
        # idpw = datajson['idpw']

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + idpw
            }
        
        data = {}
        # data = {'client_id': ID,
        #         'client_secret': SECRET,
        #         'username': USER,
        #         'password': PASSWORD,
        #         'grant_type': 'password'
        #         }
        # POST送信
        response = requests.post(
            URL,
            data=data,
            headers=headers,
            verify=False
        )
        self.res = response.text

        json_dict = json.loads(self.res)
        self.access_token = json_dict['response']['token']
        # self.access_token = response1['token']

        # self.instance_url = json_dict['instance_url']
        # self.id = json_dict['id']
        # self.token_type = json_dict['token_type']
        # self.issued_at = json_dict['issued_at']
        # self.signature = json_dict['signature']
        self.settime = datetime.datetime.now()
        print(self.access_token)

    def datareadbyID(self):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.tokenReset()
        
        url = self.URL2.format(self.serverAddress, self.databaseName, self.layoutName, 125)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + ' ' + self.access_token
        }
        
        data = {}

        response = requests.get(
            url,
            headers=headers,
            data=data,
            verify=False
        )
        res = response.text
        return res

    def datareadbyFind(self):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.tokenReset()
        
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
        res = response.text
        return res

if __name__ == '__main__':
    sf = FMDataAPI()
    print(sf.access_token)
    res1 = sf.datareadbyID()
    print(res1)
    json_dict = json.loads(res1)
    n = int(json_dict['response']['dataInfo']['returnedCount'])
    for i in range(n):
        name = json_dict['response']['data'][i]['fieldData']['顧客名']
        print(name)

    res2 = sf.datareadbyFind()
    print(res2)
    json_dict = json.loads(res2)
    n = int(json_dict['response']['dataInfo']['returnedCount'])
    for i in range(n):
        name = json_dict['response']['data'][i]['fieldData']['顧客名']
        print(name)