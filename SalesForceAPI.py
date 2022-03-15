import requests
import urllib.parse
import json
import time
import datetime

class SalesForceAPI():

    def __init__(self, *args, **kwargs):
        self.tokenReset()

    def tokenReset(self):
        URL = 'https://login.salesforce.com/services/oauth2/token'
        ID = '3MVG95mg0lk4bath12jXOUhTyb3UT.t5OLHbcUrkAecPCqR9EgZsMFGeL0C0jUtuYhOAWz2BHsq8nEc0RHOUo'
        SECRET = '028E090C53A14FCAB60943F9F96C0A9BB4F0D3B2155BEB3BC9D29F6F54518DD1'
        USER = 'kanyama@resilient-unicorn-seo0k2.com'
        PASSWORD = 'momo1momo1P61C6rfytbA3ahwrSDugOjhV4'

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

    def dataread(self):
        if datetime.datetime.now() - self.settime > datetime.timedelta(minutes=5):
            self.tokenReset()
        query = 'SELECT Name__c,Address1__c,Section_Name__c,Name FROM Customer_Data1__c WHERE Name__c LIKE \'東海カラー%\''
        url = self.instance_url + "/services/data/v54.0/query/?q=" + query
        headers = {'Authorization': self.token_type + ' ' + self.access_token}
        response = requests.get(
            url,
            headers=headers
        )
        res = response.text
        return res

if __name__ == '__main__':
    sf = SalesForceAPI()
    print(sf.access_token)
    res = sf.dataread()
    print(res)
    json_dict = json.loads(res)
    n = int(json_dict['totalSize'])
    for i in range(n):
        name = json_dict['records'][i]['Name__c']
        print(name)