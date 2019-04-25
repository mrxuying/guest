# from pymysql import cursors,connect
#
# #连接数据库
# conn = connect(host = '127.0.0.1',
#                 user='root',
#                 password='1106Never',
#                 db='guest',
#                 charset='utf8mb4',
#                 cursorclass=cursors.DictCursor)
#
# try:
#     with conn.cursor() as cursor:
#         sql = "INSERT INTO sign_guest(realname,phone,email,sign,event_id,create_time) VALUES('Iriving',18899999999,'irivisng@mail.com',0,1,Now());"
#         cursor.execute(sql)
#         conn.commit()
#     with conn.cursor() as cursor:
#         sql = "SELECT realname,phone,email,sign FROM sign_guest WHERE phone=%s;"
#         cursor.execute(sql,('18888999999'))
#         result = cursor.fetchone()
#         print(result)
# finally:
#         conn.close()

from pymysql import connect,cursors
from pymysql.err import OperationalError
import os
import configparser as cparser

##读取db_config.ini
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
# print(base_dir)
base_dir = base_dir.replace('\\','/')
file_path = base_dir + "/db_config.ini"
cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get('mysqlconf','host')
port = cf.get('mysqlconf','port')
db = cf.get('mysqlconf','db_name')
user = cf.get('mysqlconf','user')
password = cf.get('mysqlconf','password')

##封装mysql

class DB:

    def __init__(self):
        try:
            self.conn = connect(host=host,
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor)
        except OperationalError as er:
            print('mysql Error %d: %s'%(er.args[0],er.args[1]))

    ##清除数据库
    def clear(self,table_name):
        #real_sql = "truncate table" + table_name +";"
        real_sql = "delete from " + table_name + ";"
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.conn.commit()

    ##插入表数据
    def insert(self,table_name,table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) +"'"

        key = ",".join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "insert into " + table_name + " ("+key+")VALUES("+value+")"
        print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)

        self.conn.commit()

    def delete(self,table_name,value):
        real_sql = "delete from " + table_name + " where id=" + value
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)

    def select(self,table_name,value):
        real_sql = "select * from " + table_name + " where id=" + value + ";"
        print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
            result = cursor.fetchall()
            print(result)


    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = DB()
    table_name = "sign_event"
    data = {'id':12,'name':'红米','`limit`':2000,'status':1,'address':'北京会展中心','start_time':'2019-04-25 00:00:01'}
    db.insert(table_name,data)
    db.select(table_name,data['id'])
    db.delete(table_name,data['id'])
    db.close()
