import re
import urllib.request
import urllib.parse
import io
import csv

def search_by_hojinbango_sample(appid,hojinbango,jis2=False):
    """法人番号から法人情報を取得する関数サンプル
        Args:
            appid: Web-APIを利用するためのアプリケーションID（13桁）
            hojinbango: 法人番号（半角数字13桁）
            jis2: Trueのとき、文字をJIS 第一・第二水準の範囲で取得。
                 Falseのとき、文字をJIS 第一水準から第四水準の範囲で取得。
        Returns:
            法人情報のディクショナリ
    """

    # パラメータチェック
    if re.fullmatch("\\w{13}",appid) is None:
        raise Exception("13桁(半角英数字)のアプリケーションIDを指定してください")
    if re.fullmatch("\\d{13}",hojinbango) is None:
        raise Exception("13桁(半角数字)の法人番号を指定してください")
    # 応答形式：
    #   01=>CSV 形式/Shift-JIS(JIS 第一・第二水準)
    #   02=>CSV 形式/Unicode(JIS 第一水準から第四水準)
    res_type = '01' if jis2 else '02'
    # URL作成
    # version=4,id=アプリケーションID,number=法人番号,type=応答形式
    requrl = "https://api.houjin-bangou.nta.go.jp/4/num?id={}&number={}&type={}&history=0".format(
        appid,hojinbango,res_type
    )

    # 送信＋結果の処理
    with urllib.request.urlopen(requrl) as response:
        # 応答形式に応じて戻りデータをデコードする
        res_data = response.read()
        enc = "shift_jis" if jis2 else "utf-8"
        content = res_data.decode(enc)

        # csvリーダで解析
        with io.StringIO(content) as sio:
            rd = csv.reader(sio)
            # 1行目は、本サンプルではスキップ
            header = next(rd)
            # 2行目は法人情報なので、ディクショナリとして返却
            info = next(rd)
            return {
                '一連番号': info[0],
                '法人番号': info[1],
                '処理区分': info[2],
                '訂正区分': info[3],
                '更新年月日': info[4],
                '変更年月日': info[5],
                '商号又は名称': info[6],
                '商号又は名称イメージID': info[7],
                '法人種別': info[8],
                '国内所在地（都道府県）': info[9],
                '国内所在地（市区町村）': info[10],
                '国内所在地（丁目番地等）': info[11],
                '国内所在地イメージID': info[12],
                '都道府県コード': info[13],
                '市区町村コード': info[14],
                '郵便番号': info[15],
                '国外所在地': info[16],
                '国外所在地イメージID': info[17],
                '登記記録の閉鎖等年月日': info[18],
                '登記記録の閉鎖等の事由': info[19],
                '承継先法人番号': info[20],
                '変更事由の詳細': info[21],
                '法人番号指定年月日': info[22],
                '最新履歴': info[23],
                '商号又は名称（英語表記）': info[24],
                '国内所在地（都道府県）(英語表記）': info[25],
                '国内所在地（市区町村丁目番地等）（英語表記）': info[26],
                '国外所在地（英語表記）': info[27],
                'フリガナ': info[28],
                '検索対象除外': info[29]
            }

def search_by_hojinmei_sample(appid,hojinmei,jis2=False,mode="2"):
    """法人名から法人情報を取得する関数サンプル
        Args:
            appid: Web-APIを利用するためのアプリケーションID（13桁）
            hojinbango: 法人番号（半角数字13桁）
            jis2: Trueのとき、文字をJIS 第一・第二水準の範囲で取得。
                 Falseのとき、文字をJIS 第一水準から第四水準の範囲で取得。
        Returns:
            法人情報のディクショナリ
    """

    # パラメータチェック
    if re.fullmatch("\\w{13}",appid) is None:
        raise Exception("13桁(半角英数字)のアプリケーションIDを指定してください")
    # if re.fullmatch("\\d{13}",hojinbango) is None:
    #     raise Exception("13桁(半角数字)の法人番号を指定してください")
    # 応答形式：
    #   01=>CSV 形式/Shift-JIS(JIS 第一・第二水準)
    #   02=>CSV 形式/Unicode(JIS 第一水準から第四水準)
    res_type = '01' if jis2 else '02'

    hojinmei2 = urllib.parse.quote(hojinmei)
    # URL作成
    # version=4,id=アプリケーションID,number=法人番号,type=応答形式
    # requrl = "https://api.houjin-bangou.nta.go.jp/4/num?id={}&number={}&type={}&history=0".format(
    #     appid,hojinbango,res_type
    # )
    requrl = "https://api.houjin-bangou.nta.go.jp/4/name?id={}&type={}&mode={}&name={}".format(
        appid,  res_type, mode, hojinmei2
    )
    # 送信＋結果の処理
    with urllib.request.urlopen(requrl) as response:
        # 応答形式に応じて戻りデータをデコードする

        res_data = response.read()
        enc = "shift_jis" if jis2 else "utf-8"
        content = res_data.decode(enc)

        # csvリーダで解析
        with io.StringIO(content) as sio:
            rd = csv.reader(sio)
            # 1行目は、本サンプルではスキップ
            header = next(rd)
            # 2行目は法人情報なので、ディクショナリとして返却
            info = next(rd)
            return {
                '一連番号': info[0],
                '法人番号': info[1],
                '処理区分': info[2],
                '訂正区分': info[3],
                '更新年月日': info[4],
                '変更年月日': info[5],
                '商号又は名称': info[6],
                '商号又は名称イメージID': info[7],
                '法人種別': info[8],
                '国内所在地（都道府県）': info[9],
                '国内所在地（市区町村）': info[10],
                '国内所在地（丁目番地等）': info[11],
                '国内所在地イメージID': info[12],
                '都道府県コード': info[13],
                '市区町村コード': info[14],
                '郵便番号': info[15],
                '国外所在地': info[16],
                '国外所在地イメージID': info[17],
                '登記記録の閉鎖等年月日': info[18],
                '登記記録の閉鎖等の事由': info[19],
                '承継先法人番号': info[20],
                '変更事由の詳細': info[21],
                '法人番号指定年月日': info[22],
                '最新履歴': info[23],
                '商号又は名称（英語表記）': info[24],
                '国内所在地（都道府県）(英語表記）': info[25],
                '国内所在地（市区町村丁目番地等）（英語表記）': info[26],
                '国外所在地（英語表記）': info[27],
                'フリガナ': info[28],
                '検索対象除外': info[29]
            }

def print_hojinjoho_sample(appid,hojinbango,jis2=False):
    # 法人番号から法人情報を取得
    info = search_by_hojinbango_sample(appid,hojinbango,jis2)
    # 取得した情報を表示
    for k in info:
        print("{}：{}".format(k,info[k]))

def print_hojinmei_sample(appid,hojinmei,jis2=False):
    # 法人番号から法人情報を取得
    info = search_by_hojinmei_sample(appid,hojinmei,jis2)
    # 取得した情報を表示
    for k in info:
        print("{}：{}".format(k,info[k]))

if __name__ == '__main__':
    appid = "KbR2V9TieJ7um"
    hojinbango = "5120905004673"
    # hojinmei ="一般財団法人日本建築総合試験所"
    hojinmei = "株式会社りそな銀行"

    # print_hojinjoho_sample(appid,hojinbango,jis2=False)

    print_hojinmei_sample(appid, hojinmei, jis2=False)