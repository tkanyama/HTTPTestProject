import urllib
import urllib.request
import base64

url = "http://localhost:8080/upload"
encoding = "utf-8"
boundary = "--------python"

f = open("image.png", "rb", buffering=0)
file_data = f.read()
f.close()

def multipart_formdata():
    value = '--' + boundary
    value += 'Content-Disposition: form-data; name="message"'
    value += ''
    value += 'hello'
    value += '--' + boundary
    value += 'Content-Disposition: form-data; name="uploadfile"; filename="image.png"'
    value += 'Content-Type: image/png'
    value += 'Content-Transfer-Encoding: base64'
    value += ''
    value += str(base64.b64encode(file_data))
    value += ''
    value += "--" + boundary + "--"
    value += ''

    return value.encode(encoding)

def request_with_multipart_formdata():
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
    data = multipart_formdata()
    with urllib.request.urlopen(req, data) as response:
        print(response.status)

request_with_multipart_formdata()