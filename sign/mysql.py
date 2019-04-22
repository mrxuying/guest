from pymysql import cursors,connect

#连接数据库
conn = connect(host = '127.0.0.1',
                user='root',
                password='1106Never',
                db='guest',
                charset='utf8mb4',
                cursorclass=cursors.DictCursor)

try:
    with conn.cursor() as cursor:
        sql = "INSERT INTO sign_guest(realname,phone,email,sign,event_id,create_time) VALUES('Iriving',18899999999,'irivisng@mail.com',0,1,Now());"
        cursor.execute(sql)
        conn.commit()
    with conn.cursor() as cursor:
        sql = "SELECT realname,phone,email,sign FROM sign_guest WHERE phone=%s;"
        cursor.execute(sql,('18888999999'))
        result = cursor.fetchone()
        print(result)
finally:
        conn.close()
