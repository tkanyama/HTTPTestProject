import re
import urllib.request
import urllib.parse
import io
import csv

def create_request():
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

if __name__ == '__main__':
    req = create_request()
    with urllib.request.urlopen(req) as res:
        html = res.read().decode('utf-8')
        print(html)