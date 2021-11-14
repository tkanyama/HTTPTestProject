import requests
import urllib.parse

file_path_name = '/Users/tkanyama/Google ドライブ/Work/情報システムWG/経理課関連/顧客データ/顧客20211112.csv'
file_path_name2 = urllib.parse.quote(file_path_name)
#POSTするURL設定
post_url = "https://ta.eco-serv.jp/gbrc/api/v1/customers/imports"

#POSTするデータ設定

# data = {"json":("",{"ispdatenfo": 0,
#             "updateBlank": 2,
#             "importProcessName": "顧客データ取込サンプル",
#             "skipFirst": 1,
#             "settingId": 5
#          },"application/json")}
# json_data = { "col1": "val1",
#               "col2": "val2",
#               "col3": "val3",
#               "col4": data
#             }
#POSTするファイルsの読込
# files = { "files[0]": ("顧客20211112.csv",open(file_path_name, 'r', encoding='shift_jis'),'text/csv') }#ヘッダー設定
files = { "json":("",{"ispdatenfo": "0",
            "updateBlank": "2",
            "importProcessName": "顧客データ取込サンプル",
            "skipFirst": "1",
            "settingId": "5"
         },"application/json"),
    "file": ("顧客20211112.csv",open(file_path_name, 'r', encoding='shift_jis'),'text/csv') }#ヘッダー設定
headers = {
            'X-WB-apitoken': 'AZsH5M76XPXASjHAkEcIGOKtfjUL46CXrpadiQJfh9srDghuGLp6hxXC0DTfegbK'
            }

#POST送信
response = requests.post(
    post_url,
    # data = data,
    files = files,
    headers = headers)

print(response)
print("OK")