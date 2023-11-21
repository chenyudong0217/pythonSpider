# encoding:utf-8
import sys
import mysql.connector

cnx = None
cursor = None
class mysql_util:
    host = ''
    port = ''
    user = ''
    password = ''
    database = ''
    cnx = None
    #构造mysql_util 类，初始化连接对象
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.cnx = mysql.connector.connect(
            host = host, # 链接地址
            port = port,
            user = user, # 登录名
            password = password, # 登录密码
            database = database # 链接数据
        )

    #获取数据库连接对象
    def get_connector(self):
        try:
            if self.cnx == None:
                self.cnx = mysql.connector.connect(self.host,self.port,self.user, self.password, self.database)
            cursor = self.cnx.cursor()
            return cursor
        except Exception as e:
            print(e)
        return None

    #新增数据
    def insert_data(self, sql):
        try:
            cursor = self.get_connector()
            cursor.execute(sql)
            self.cnx.commit()
            #cursor.close()
        except Exception as e:
            print(e)

    #查询数据
    def select_data(self, sql):
        try:
            cursor = self.get_connector()
            cursor.execute(sql)
            result = cursor.fetchall();
            #cursor.close();
            return result
        except Exception as e:
            print(e)

    def update_data(self, sql):
        try:
            cursor = self.get_connector()
            cursor.execute(sql)
            self.cnx.commit()
            #cursor.close();
        except Exception as e:
            print(e)
    def del_data(self,sql):
        try:
            cursor = self.get_connector()
            cursor.execute(sql)
            self.cnx.commit()
        except Exception as e:
            print(e)
if __name__ == '__main__':
    print('start test mysql')
    mysql_util = mysql_util('localhost',3306,'root','root','pkulaw')
    result = mysql_util.select_data('select * from account_table')
    for account in result:
        print(account[5])
