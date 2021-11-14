
import urllib
import urllib.request
import csv
url = "https://ta.eco-serv.jp/gbrc/api/v1/customers/imports"
encoding1 = "utf-8"
encoding2 = "shift_jis"
boundary = "--------python"
file_path_name = '/Users/tkanyama/Google ドライブ/Work/情報システムWG/経理課関連/顧客データ/顧客20211112.csv'
jsondata = '{'
jsondata += '"ispdatenfo": "0",'
jsondata += '"updateBlank": "2",'
jsondata += '"importProcessName": "顧客データ取込サンプル",'
jsondata += '"skipFirst": "1",'
jsondata += '"settingId": "5"'
jsondata += '}'


def multipart_formdata():
    lines = []

    lines.append('')
    lines.append('--' + boundary )
    lines.append('Content-Disposition: form-data; name="json"')
    lines.append('Content-Type: application/json; charset=UTF-8')
    lines.append('')
    lines.append(jsondata)

    lines.append('--' + boundary )
    lines.append('Content-Disposition: form-data; name="files[0]"; filename="顧客20211112.csv"')
    lines.append('Content-Type: text/csv')
    lines.append('')
    value1 = "\r\n".join(lines)

    lines = []
    lines.append('')
    csv_file = open(file_path_name, "r", encoding="shift_jis", errors="", newline="")
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                   skipinitialspace=True)
    header = next(f)
    print(header)
    l1 = ""
    n=len(header)
    i = 0
    for d in header:
        i += 1
        l1 += '"'+d + '"'
        if i<n:
            l1 += ','
    print(l1)
    lines.append(l1)
    for row in f:
        print(row)
        l1 = ""
        n = len(row)
        i = 0
        for d in row:
            i += 1
            l1 += '"' + d + '"'
            if i < n:
                l1 += ','
        print(l1)
        lines.append(l1)
    value2 = "\r\n".join(lines)
    #
    lines = []
    lines.append('')
    lines.append("--" + boundary + "--" )
    value3 = '\r\n'.join(lines)

    value = value1.encode(encoding1) + value2.encode(encoding2) + value3.encode(encoding1)
    print(value)
    print("OK")
    # return value.encode(encoding1)
    return value

def request_with_multipart_formdata():
    req = urllib.request.Request(url)
    req.add_header('X-WB-apitoken', 'AZsH5M76XPXASjHAkEcIGOKtfjUL46CXrpadiQJfh9srDghuGLp6hxXC0DTfegbK')
    req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
    data = multipart_formdata()
    with urllib.request.urlopen(req, data) as response:
        print(response.status)
    print(data)

request_with_multipart_formdata()