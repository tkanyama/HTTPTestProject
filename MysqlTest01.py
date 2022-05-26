import mysql.connector
from mysql.connector import errorcode


# conn = mysql.connector.connect(user='tkanyama', password='momo1momo1',host ='192.168.32.81', database='world')
#
# print(conn.is_connected())
# conn.close()

class MySqlAPI():
    def __init__(self, *args, **kwargs):
        self.user = 'tkanyama'
        self.password = 'momo1momo1'
        self.host = '192.168.32.81'

        self.set_config(
            user=self.user, password=self.password, host=self.host)

    def set_config(self, user='tkanyama', password='momo1momo1', host='192.168.32.81'):
        self.user = user
        self.password = password
        self.host = host
        self.config = {
            'user': self.user,
            'password': self.password,
            'host': self.host
        }

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def sqlexecute(self, sql_str="SELECT * FROM city WHERE CountryCode = 'JPN'"):
        cur = self.conn.cursor(buffered=True, dictionary=True)
        cur.execute(sql_str)
        rows = cur.fetchall()

        # cur.execute("DESC テーブル名")
        # rows = cur.fetchall()
        return rows

    def databasenames(self):
        # データベース一覧を取得
        cur = self.conn.cursor()
        cur.execute("SHOW DATABASES")
        rows = cur.fetchall()
        return rows

    def tablenames(self):
        # データベース一覧を取得
        cur = self.conn.cursor()
        cur.execute("SHOW TABLES")
        rows = cur.fetchall()
        return rows

    def changedatabase(self, database='world'):
        cur = self.conn.cursor()
        cur.execute('USE {}'.format(database))
        # rows = cur.fetchall()
        # return rows

    def fieldnames(self, tablename='city'):
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
                   host='192.168.32.81'
                   )
    if my1.connect():

        databases = my1.databasenames()
        for databese in databases:
            if databese[0] != 'information_schema' and databese[0] != 'mysql' and databese[0] != 'performance_schema':
                print("***********************")
                print("  databesename = {}".format(databese[0]))
                print("***********************")
                print("")
                my1.changedatabase(databese[0])
                tablenames = my1.tablenames()
                n = len(tablenames)

                for tabelname in tablenames:
                    print("***********************")
                    print("  tablename = {}".format(tabelname[0]))
                    print("***********************")
                    fields = my1.fieldnames(tablename=tabelname[0])
                    n = fields.__len__()
                    i = 0
                    for field in fields:
                        i += 1
                        print(field[0], end='')
                        if i < n:
                            print(' , ', end='')
                    print('')

                    sql_str1 = "SELECT * FROM {} LIMIT 10".format(tabelname[0])
                    rows = my1.sqlexecute(sql_str=sql_str1)
                    for row in rows:
                        i = 0
                        for field in fields:
                            i += 1
                            print(row[field[0]], end='')
                            if i < n:
                                print(' , ', end='')

                        print('')

                    print('')
        my1.close()
