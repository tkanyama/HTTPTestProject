from multiprocessing.resource_sharer import stop
import requests
import urllib.parse
import json
import time
import datetime
import os.path
import base64
import sys
# print(base64.b64encode('こんにちは'.encode()))

class FMDataAPI():

    def __init__(self, serverAddress, databaseName, layoutName):
        if not self.RMDataAPILogin(serverAddress, databaseName, layoutName):            
            sys.exit()



    def RMDataAPILogin(self, serverAddress, databaseName, layoutName):

        # IDとパスワードをJsonファイルから読み込む
        path = os.path.expanduser('~/init2.json')
        f = open(path, 'r')
        datajson = json.loads(f.read())
        f.close()
        self.USER = datajson['USER']
        self.PASSWORD = datajson['PASSWORD']
        # "ID:Password"をBase64にエンコード（binary）し、さらに、文字列にデコード
        self.idpw = base64.b64encode((self.USER + ':' + self.PASSWORD).encode()).decode()

        # self.serverAddress = "192.168.0.171"
        # self.databaseName = "楽楽明細"
        # self.layoutName = "顧客リスト"

        self.serverAddress = serverAddress
        self.databaseName = databaseName
        self.layoutName = layoutName
        
        self.URL1 = "https://{}/fmi/data/vLatest/databases/{}/sessions"
        self.URL2 = "https://{}/fmi/data/vLatest/databases/{}//layouts/{}/records/{}"
        self.URL3 = "https://{}/fmi/data/vLatest/databases/{}//layouts/{}/_find"

        self.URL4 = "https://{}/fmi/data/vLatest/productInfo".format(self.serverAddress)
        response = requests.get(
            self.URL4,
            headers={},
            json = {},
            verify=False
        )
        if response.status_code == 200:
            json_dict = json.loads(response.text)
            self.dateFormat = json_dict['response']["productInfo"]['dateFormat']
            self.timeStampFormat = json_dict['response']["productInfo"]['timeStampFormat']
            self.timeFormat = json_dict['response']["productInfo"]['timeFormat']

           

        # RestAPIで通信可能なデータベース名を取得
        self.databases = self.readDatabaseName()

        URL = self.URL1.format(self.serverAddress, self.databaseName)

 
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

            # データベースに含まれるスクリプト名をすべて取得
            self.scripts = self.readScriptName()
            # データベースに含まれるレオアウト名をすべて取得
            self.layouts = self.readLyoutName()
            
            # 指定されたデータベースやレイアウトが実際にあるかどうかチェックする
            if (self.databaseName in self.databases) and (self.layoutName in self.layouts):
                return True
            else:
                print("データベースまたはレイアウトが存在しません!!\n 終了します!!")
                return False

        else:
            res = ""
            self.access_token = ""
            return False
            
    def RMDataAPILogOut(self):

        URL = self.URL1.format(self.serverAddress, self.databaseName) + '/' + self.access_token
 
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.idpw
            }
        
       # DELETE送信
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

    def readDatabaseName(self):

        self.URL5 = "https://{}/fmi/data/vLatest/databases".format(self.serverAddress)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.idpw
            }
        response = requests.get(
            self.URL5,
            headers=headers,
            json = {},
            verify=False
        )
        names = []
        if response.status_code == 200:
            res = response.text
            json_dict = json.loads(res)
            databases = json_dict['response']["databases"]
            for database in databases:
                names.append(database['name'])
                print(database['name'])
  
        return names

    def readScriptName(self):

        self.URL6 = "https://{}/fmi/data/vLatest/databases/{}/scripts".format(self.serverAddress, self.databaseName)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + ' ' + self.access_token
        }

        response = requests.get(
            self.URL6,
            headers=headers,
            json = {},
            verify=False
        )
        names = []
        if response.status_code == 200:
            res = response.text
            json_dict = json.loads(res)
            scripts = json_dict['response']["scripts"]
            for script in scripts:
                names.append(script['name'])
                print(script['name'])
  
        return names

    def readLyoutName(self):

        self.URL7 = "https://{}/fmi/data/vLatest/databases/{}/layouts".format(self.serverAddress, self.databaseName)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + ' ' + self.access_token
        }

        response = requests.get(
            self.URL7,
            headers=headers,
            json = {},
            verify=False
        )
        names = []
        if response.status_code == 200:
            res = response.text
            json_dict = json.loads(res)
            layouts = json_dict['response']["layouts"]
            for layout in layouts:
                names.append(layout['name'])
                print(layout['name'])
  
        return names


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

    serverAddress = "192.168.0.171"
    databaseName = "楽楽明細"
    layoutName = "顧客リスト"
    sf = FMDataAPI(serverAddress, databaseName ,layoutName)

    # databases = sf.readDatabaseName()
    # print(sf.access_token)
    res1 = sf.datareadbyID()
    if res1 != "":
        # print(res1)
        json_dict = json.loads(res1)
        
        n = int(json_dict['response']['dataInfo']['returnedCount'])
        for i in range(n):
            name = json_dict['response']['data'][i]['fieldData']['顧客名']
            print(name)
            keys = json_dict['response']['data'][i]['fieldData'].keys()
            print(keys)
            for key in keys:
                print(key , ':' ,json_dict['response']['data'][i]['fieldData'][key])

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