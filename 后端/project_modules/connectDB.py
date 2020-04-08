import pymysql

connection=pymysql.connect(host='127.0.0.1',user='root',password='root',database='db1',charset='utf8')
cursor=connection.cursor()
cursor.execute("create table t3(id int primary key,name char(20));")
# connection.commit()
cursor.close()
connection.close()