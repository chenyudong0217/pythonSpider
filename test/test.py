# encoding: utf-8
import json,re
from src.util.mysqlUtil import mysql_util
mysqlUtil = mysql_util('localhost',3306,'root','root','pkulaw')

if __name__ == '__main__':
    with open('www_flfg.txt','r', encoding='utf-16') as file:
        index = 0
        for line in file:
            print(line)#name="currGid" value="d9621f59b24d5128bdfb"
            value = re.search('logother=\"(.*?)\" name=\"faxian\"',line)
            if value != None:
                law_id_title = value.group(1)
                if law_id_title.__contains__('、'):
                    law_id = law_id_title.split('、')[0]
                    title = law_id_title.split('、')[1]
                    insert_law_sql = "insert into law_id_table (topic_id, column_id,law_id,title, is_crawled) values ('1469238631649644544', '1469238638146621440', '"+law_id+"','"+title+"', 0);"
                    mysqlUtil.insert_data(insert_law_sql)
                    index = index+1
        print(index)

    with open('flfg.txt','r',encoding='utf-16') as file:
        for line in file:
            try:
                result = json.loads(line)
                if result['code'] == 200:
                    laws = result['data']['info']
                    for law in laws:
                        print(law)
                        insert_law_sql = "insert into law_id_table (topic_id, column_id,law_id, title, is_crawled) values ('"+law['topicId']+"', '"+law['columnId']+"', '"+law['gid']+"', '"+law['title']+"', 0);"
                        mysqlUtil.insert_data(insert_law_sql)

            except Exception as e:
                print(e)

