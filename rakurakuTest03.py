import requests
import urllib.parse
import json
from io import BytesIO

file_path_name = '/Users/tkanyama/マイドライブ/Work/情報システムWG/経理課関連/VBAサンプルプログラム3_2/サンプルデータ/帳票データ/テスト用データ.zip'
file_path_name2 = '/Users/tkanyama/マイドライブ/Work/情報システムWG/経理課関連/VBAサンプルプログラム3_2/サンプルデータ/帳票データ/帳票データ_Zip.csv'
#POSTするURL設定
post_url = "https://rbthyme.eco-serv.jp/gbrc/api/v1/reports/imports"

#POSTするデータ設定
# {"approvalFlowId":3,"importProcessName":"テスト送信","isImmApproval":0,"reportTypeId":14,"skipFirst":1}
json1 = {
            "approvalFlowId": 3,
            "importProcessName": "テスト送信",
            "isImmApproval":0,
            "reportTypeId":14,
            "skipFirst": 1
         }
json2 = BytesIO(json.dumps(json1,ensure_ascii = False).encode('utf-8'))
data={ "json":json2 }

with open(file_path_name2, 'r' ,encoding='shift_jis') as f:
    csvdata = f.read()
readdata = BytesIO(csvdata.encode('shift_jis'))
#POSTするファイルsの読込
# filepath = "/Users/tkanyama/マイドライブ/Work/情報システムWG/経理課関連/VBAサンプルプログラム3_2/サンプルデータ/顧客データ/顧客データ1.csv"
files = {
    "files[1]": ("帳票データ_Zip.csv", readdata, "text/csv; charset=Windows-31J"),
    "files[0]": ("テスト用データ.zip",open(file_path_name, 'rb'),"application/zip")
}#ヘッダー設定

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