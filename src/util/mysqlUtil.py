# encoding:utf-8
import mysql.connector

def init():
    cnx = mysql.connector.connect(
        host='localhost:3306', # 链接地址
        user='root', # 登录名
        password='root', # 登录密码
        database='pkulaw' # 链接数据
    )
    cursor = cnx.cursor()
    return cursor

if __name__ == '__main__':

