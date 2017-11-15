import MySQLdb

conn = MySQLdb.connect("10.10.7.58","xiaoyi","ApK1e1iMyqCprb8z","test" )
cursor = conn.cursor()
# 创建user表:
cursor.execute('create table IF NOT EXISTS user (id varchar(20) primary key, name varchar(20))')
# 插入一行记录，注意MySQL的占位符是%s:
cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Michael'])
print cursor.rowcount
conn.commit()
cursor.close()

# 运行查询:
cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ('1',))
values = cursor.fetchall()
print values
# 关闭Cursor和Connection:
cursor.close()
conn.close()