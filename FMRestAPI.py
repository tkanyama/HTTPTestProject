import json
import os.path
import fmrest


def savePDF(url, fms , filename):
    name, type_, length, response = fms.fetch_file(url, stream=True)
    with open(filename, 'wb') as file_:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                file_.write(chunk)
    response.close()

if __name__ == '__main__':
# IDとパスワードをJsonファイルから読み込む
    path = os.path.expanduser('~/init2.json')
    f = open(path, 'r')
    datajson = json.loads(f.read())
    f.close()
    USER = datajson['USER']
    PASSWORD = datajson['PASSWORD']
    serverAddress = "192.168.0.171"
    databaseName = "総務課文書管理"
    layoutName = "文書単票"
   
    fms = fmrest.Server("https://{}".format(serverAddress),
                user=USER,
                password=PASSWORD,
                database=databaseName,
                layout=layoutName,
                api_version='vLatest',
                verify_ssl=False
                )
    fms.login()
    print(fms)
    databases = fms.get_databases()
    lyouts = fms.get_layouts()

    res1 = fms.get_record(160)
    dic = res1.to_dict()
    keys = res1.keys()
    v1 = res1.values()
    
    for key in keys:
        print(key, ":",dic[key])
        if key == "PDF":
            savePDF(dic[key], fms , "/Users/kanyama/PDF/test2.pdf")

    res2 = fms.get_records(limit=2)
    n=0
    for res in res2:
        dic = res.to_dict()
        keys = res.keys()
        v1 = res.values()
        id = int(dic["recordId"])
        for key in keys:
            print(key, ":",dic[key])
            if key == "PDF":
                n += 1
                # fname = '/Users/kanyama/PDF/test{0:05}.pdf'.format(id)
                savePDF(dic[key], fms , "/Users/kanyama/PDF/書類{0:05}.pdf".format(id))

    find_query = [
                {"作成日": "09/01/1971","分類": "役員会議事録" }
                ]

    order_by = [
        {"fieldName": "作成日","sortOrder": "ascend" }
        ] 

    res3 = fms.find(find_query, sort=order_by)
    for res in res3:
        dic = res.to_dict()
        keys = res.keys()
        v1 = res.values()
        for key in keys:
            print(key, ":",dic[key])

    fms.logout()