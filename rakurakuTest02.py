import requests
import urllib.parse

file_path_name = '/Users/kanyama/Google ドライブ/Work/情報システムWG/経理課関連/顧客データ/cust_20211110.csv'
file_path_name2 = urllib.parse.quote(file_path_name)
#POSTするURL設定
post_url = "https://ta.eco-serv.jp/gbrc/api/v1/customers/imports"

#POSTするデータ設定
# data = {[{"data_col1": "data1-1",
#           "data_col2": "data2-1",
#           "data_col3": "data3-1"},
#          {"data_col1": "data1-2",
#           "data_col2": "data2-2",
#           "data_col3": "data3-2"},
#          {"data_col1": "data1-3",
#           "data_col2": "data2-3",
#           "data_col3": "data3-3"}
#          ]}
# json_data = { "col1": "val1",
#               "col2": "val2",
#               "col3": "val3",
#               "col4": data
#             }
#POSTするファイルsの読込
# files = { "image_file": open(file_path_name, 'rb') }#ヘッダー設定
headers = {
            'X-WB-apitoken': 'AZsH5M76XPXASjHAkEcIGOKtfjUL46CXrpadiQJfh9srDghuGLp6hxXC0DTfegbK',
            'Content-Type': 'multipart/form-data' ,
            'Content-Disposition': 'form-data; name="files[0]" ; filename="' + file_path_name + '"' ,
            'Content-Type': 'text/csv'
            }

#POST送信
response = requests.post(
    post_url,
    # data = json_data,
    # files = files,
    headers = headers)

print("OK")