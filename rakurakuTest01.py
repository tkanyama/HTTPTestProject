import re
import urllib.request
import urllib.parse
import io
import csv

def create_request1():
    domain = "ta.eco-serv.jp"
    acount = "gbrc"
    key = "事務局"
    key2 = urllib.parse.quote(key)
    requrl = "https://{}/{}/api/v1/customers/?keyword={}".format(
        domain, acount, key2
    )
    req = urllib.request.Request(requrl)
    req.add_header('X-WB-apitoken', 'AZsH5M76XPXASjHAkEcIGOKtfjUL46CXrpadiQJfh9srDghuGLp6hxXC0DTfegbK')
    return req

def create_request2(id):
    domain = "ta.eco-serv.jp"
    acount = "gbrc"
    requrl = "https://{}/{}/api/v1/customers/?keyword={}".format(
        domain, acount, id
    )
    req = urllib.request.Request(requrl)
    req.add_header('X-WB-apitoken', 'AZsH5M76XPXASjHAkEcIGOKtfjUL46CXrpadiQJfh9srDghuGLp6hxXC0DTfegbK')
    return req

def create_request3(id):
    domain = "ta.eco-serv.jp"
    acount = "gbrc"
    requrl = "https://{}/{}/api/v1/reports/export/download/?keyword={}".format(
        domain, acount, id
    )
    req = urllib.request.Request(requrl)
    req.add_header('X-WB-apitoken', 'AZsH5M76XPXASjHAkEcIGOKtfjUL46CXrpadiQJfh9srDghuGLp6hxXC0DTfegbK')
    return req

if __name__ == '__main__':
    req = create_request1()
    with urllib.request.urlopen(req) as res:
        html = res.read().decode('utf-8')
        html = urllib.parse.unquote(html)
        print(html)

    req = create_request2("9999")
    with urllib.request.urlopen(req) as res:
        html = res.read().decode('utf-8')
        print(html)

    req = create_request3("SOUMU001")
    # urllib.request.urlretrieve(req,
    #                            "sample.zip")
    # from urllib.request import urlopen
    from shutil import copyfileobj

    # url="https://laboratory.kazuuu.net/wp-content/uploads/2020/10/mov_hts-samp003.mp4"

    with urllib.request.urlopen(req) as input_file, open('sample2.zip','wb') as output_file:
        print("ダウンロード中")
        copyfileobj(input_file, output_file)
        print("ダウンロードが完了しました。")