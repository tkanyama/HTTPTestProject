import mysql.connector
from mysql.connector import errorcode


# conn = mysql.connector.connect(user='tkanyama', password='momo1momo1',host ='192.168.32.81', database='world')
#
# print(conn.is_connected())
# conn.close()

class MySqlAPI():
    def __init__(self, *args, **kwargs):
        self.config = {
            'user': 'tkanyama',
            'password': 'momo1momo1',
            'host': '192.168.32.81',
            'database': 'world'
        }

    def set_config(self, user='tkanyama', password='momo1momo1', host='192.168.32.81', database='world'):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def select(self, sql_str="SELECT * FROM city WHERE CountryCode = 'JPN'"):
        cur = self.conn.cursor(buffered=True, dictionary=True)
        cur.execute(sql_str)
        rows = cur.fetchall()

        # cur.execute("DESC テーブル名")
        # rows = cur.fetchall()
        return rows

    def fieldname(self, tablename='city'):
        # フィールド一覧を取得
        cur = self.conn.cursor()
        cur.execute("DESC " + tablename)
        rows = cur.fetchall()
        return rows

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    my1 = MySqlAPI()
    my1.set_config(user='tkanyama',
                   password='momo1momo1',
                   host='192.168.32.81',
                   database='world'
                   )
    if my1.connect():
        sql_str1 = "SELECT * FROM city WHERE CountryCode = 'JPN' AND District='Osaka'"
        rows = my1.select(sql_str=sql_str1)
        print(rows.__len__())
        fields = my1.fieldname(tablename='city')
        n = fields.__len__()
        i = 0
        for f in fields:
            i += 1
            print(f[0], end='')
            if i < n:
                print(' , ', end='')
        print('')

        for row in rows:
            i = 0
            for f in fields:
                i += 1
                print(row[f[0]], end='')
                if i < n:
                    print(' , ', end='')

            print('')
        my1.close()
