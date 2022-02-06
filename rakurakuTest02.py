import requests
import urllib.parse
import json
from io import BytesIO

file_path_name = '/Users/tkanyama/マイドライブ/Work/情報システムWG/経理課関連/VBAサンプルプログラム3_2/サンプルデータ/顧客データ/顧客データ1.csv'
file_path_name2 = urllib.parse.quote(file_path_name)
#POSTするURL設定
post_url = "https://rbthyme.eco-serv.jp/gbrc/api/v1/customers/imports"

#POSTするデータ設定
json1 = {
            "isUpdateInfo": 1,
            "updateBlank": 2,
            "importProcessName": "顧客データ取込サンプル",
            "skipFirst": 1 ,
            "settingId": 5
         }
json2 = BytesIO(json.dumps(json1,ensure_ascii = False).encode('utf-8'))
data={ "json":json2 }

#POSTするファイルsの読込
filepath = "/Users/tkanyama/マイドライブ/Work/情報システムWG/経理課関連/VBAサンプルプログラム3_2/サンプルデータ/顧客データ/顧客データ1.csv"
with open(file_path_name, 'r' ,encoding='shift_jis') as f:
    csvdata = f.read()
readdata = BytesIO(csvdata.encode('shift_jis'))
files = { "files[0]": ("顧客データ1.csv",readdata,"text/csv; charset=Windows-31J") }

#ヘッダー設定
headers = {
            "X-WB-apitoken": "AZsH5M76XPXASjHAkEcIGOKtfjUL46CXrpadiQJfh9srDghuGLp6hxXC0DTfegbK"
            }
#POST送信
response = requests.post(
    post_url,
    data = data,
    files = files,
    headers = headers)

print(response.text)
print("OK")