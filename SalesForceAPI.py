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
        # POST送信
        response = requests.post(
            URL,
            data=data
        )
        self.res = response.text

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

    def dataread(self):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.tokenReset()
        query = 'SELECT Name__c,Address1__c,Section_Name__c,Name FROM Customer_Data1__c WHERE Name__c LIKE \'東海カラー%\''
        # url = self.instance_url + self.url + "/query/?q=" + query
        # headers = {'Authorization': self.token_type + ' ' + self.access_token}
        response = requests.get(
            self.instance_url + self.url + "/query/?q=" + query,
            headers={'Authorization': self.token_type + ' ' + self.access_token}
        )
        res = response.text
        return res

    def mataDataRead(self, sObject="Customer_Data1__c"):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.tokenReset()
        # query = 'SELECT Name__c,Address1__c,Section_Name__c,Name FROM Customer_Data1__c WHERE Name__c LIKE \'東海カラー%\''
        # url = self.instance_url + self.url + "/sobjects/" + sObject + "/"
        # headers = {'Authorization': self.token_type + ' ' + self.access_token}
        response = requests.get(
            self.instance_url + self.url + "/sobjects/" + sObject + "/",
            headers={'Authorization': self.token_type + ' ' + self.access_token}
        )
        res = response.text
        return res

    def version(self):
        # url = self.instance_url + "/services/data" 
        response = requests.get(
            self.instance_url + "/services/data",
        )
        res = response.text
        return res

    def getResourse(self):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.tokenReset()
        # query = 'SELECT Name__c,Address1__c,Section_Name__c,Name FROM Customer_Data1__c WHERE Name__c LIKE \'東海カラー%\''
        # url = self.instance_url + self.url
        # headers = {'Authorization': self.token_type + ' ' + self.access_token}
        response = requests.get(
            self.instance_url + self.url,
            headers={'Authorization': self.token_type + ' ' + self.access_token}
        )
        res = response.text
        return res

    def getObjectList(self):
            if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
                self.tokenReset()
  
            response = requests.get(
                self.instance_url + self.url + "/sobjects/",
                headers={'Authorization': self.token_type + ' ' + self.access_token,
                'X-PrettyPrint':'1'}
            )
            res = response.text
            return res

    def getObjecInfo(self, sObject="Customer_Data1__c"):
            if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
                self.tokenReset()
  
            response = requests.get(
                self.instance_url + self.url + "/sobjects/" + sObject + "/",
                headers={'Authorization': self.token_type + ' ' + self.access_token,
                'X-PrettyPrint':'1'}
            )
            res = response.text
            return res


if __name__ == '__main__':
    sf = SalesForceAPI()
    print(sf.access_token)

# APIのバージョンを取得
    res = sf.version()
    data = json.loads(res)
    n = len(data)
    sf.url = data[n-2]["url"]   # 最新のひとつ前のバージョンを指定
    print(sf.url)

    res = sf.getResourse()
    sf.resourse = json.loads(res)
    print(json.dumps(data, indent=4))

    res = sf.getObjectList()
    # print(res)
    data = json.loads(res)
    print(json.dumps(data, indent=4))

    res = sf.getObjecInfo("Customer_Data1__c")
    # print(res)
    data = json.loads(res)
    print(json.dumps(data, indent=4))

    res = sf.mataDataRead("Customer_Data1__c")
    # print(res)
    data = json.loads(res)
    print(json.dumps(sf.resourse, indent=4))

    res = sf.dataread()
    print(res)
    json_dict = json.loads(res)
    n = int(json_dict['totalSize'])
    for i in range(n):
        name = json_dict['records'][i]['Name__c']
        print(name)