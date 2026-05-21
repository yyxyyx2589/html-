import pymysql
from pyarrow import null

'''print(pymysql.__version__)

conn= pymysql.connect(
    host='localhost',
    user='root',
    passwd='1234',
    db='school'
)
print("连接成功")
conn.close()


try:
    conn=pymysql.connect(
        host='localhost',
        user='root',
        passwd='123',
        db='school'
    )
    print("连接成功")
except pymysql.MySQLError as e:
    print('Error:',e)

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='1234',
        db='school'
    )
    cursor = conn.cursor()
    cursor.execute('select * from students')
    result = cursor.fetchall()
except pymysql.MySQLError as e:
    print('Error:',e)
finally:
    cursor.close()
    conn.close()'''

"""try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='1234',
        db='company2'
    )
    cursor = conn.cursor()
    sql="insert into employees(emp_name,salary) values(%s,%s)"
    cursor.executemany(sql)
    conn.commit()
    print(f"插入成功，影响行数:{cursor.rowcount}")

    select_sql="select * from employees"
    cursor.execute(select_sql)
    result = cursor.fetchall()
    for row in result:
        print(row)

except pymysql.MySQLError as e:
    print('Error:',e)
finally:
    cursor.close()
    conn.close()"""


"""def create_table(cursor,conn):
    sql="""
    #create table if not exists users4(
     #   id int primary key auto_increment,
      #  username varchar(20) not null,
       # gender enum('男','女') default('男'),
        #phone varchar(20) not null)
"""
    cursor.execute(sql)
    conn.commit()
    print("创表成功")

def insert_(cursor,conn):
    sql="insert into users4(username,gender,phone) values(%s,%s,%s)"
    name=input("要插入的姓名:")
    gender = input("要插入的性别:")
    phone = input("要插入的电话:")
    cursor.execute(sql,(name,gender,phone))
    conn.commit()
    print("插入成功")

def select_all(cursor):
    print("所有内容:")
    sql=("select * from users4")
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)


def select_man(cursor):
    print("查询所有男性用户")
    sql=("select * from users4 where gender='男'")
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)
    print("查询成功")

def modify_phone(cursor,conn):
    sql=("update users4 set phone=%s where username=%s")
    name = input("输入要修改的姓名:")
    phone = input("输入要修改的电话:")
    cursor.execute(sql, (phone, name))
    conn.commit()
    print("修改手机号成功")
    select_all(cursor)

def delete_id(cursor,conn):
    sql=("delete from users4 where id=%s")
    id=input("输入要删除的id:")
    cursor.execute(sql,id)
    conn.commit()
    print("删除id成功")
    select_all(cursor)


while True:
    print("1:建表")
    print("2:插入数据")
    print("3:显示所有")
    print("4:查询男用户")
    print("5:修改电话号")
    print("6:删除id")
    print("7:退出")
    choice=int(input())
    try:
        conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = '1234',
            db = 'company2',
            autocommit = False
        )
        cursor = conn.cursor()
        if choice==1:
            create_table(cursor,conn)
        if choice==2:
            insert_(cursor,conn)
        if choice==3:
            select_all(cursor)
        if choice==4:
            select_man(cursor)
        if choice==5:
            modify_phone(cursor,conn)
        if choice==6:
            delete_id(cursor, conn)
        if choice==7:
            break

    except pymysql.MySQLError as e:
        print("error:",e)
    finally:
        cursor.close()
        conn.close()"""


"""try:
    conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        passwd = '1234',
        db = 'company2',
        autocommit = False
    )
    cursor = conn.cursor()

    sql="update employees set salary=salary-500 where emp_name=%s"
    cursor.execute(sql,'小明')

    sql2="update employees set salary=salary+500 where emp_name=%s"
    cursor.execute(sql, '小红')

    conn.commit()
    print("操作成功")

    select_sql="select * from employees"
    cursor.execute(select_sql)
    result = cursor.fetchall()
    for row in result:
        print(row)

except pymysql.MySQLError as e:
    print("error:",e)
finally:
    cursor.close()
    conn.close()"""


import pymysql
class DBHelper:
    def __init__(self,host,user,pwd,db):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=pwd,
            database=db,
            charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def query(self,sql,param=None):
        self.cursor.execute(sql,param or ())
        return self.cursor.fetchall()

    def execute(self,sql,param=None):
        try:
            self.cursor.execute(sql,param or ())
            return self.conn.commit()
        except pymysql.MySQLError as e:
            self.conn.rollback()
            raise e

    def close(self):
        if self.conn:
            self.conn.close()
        if self.cursor:
            self.cursor.close()

class UserManager:
    def __init__(self,db_helper):
        self.db=db_helper

    def add_user(self,username,gender,phone):
        sql="insert into users4(username,gender,phone) values(%s,%s,%s)"
        self.db.execute(sql,(username,gender,phone))
        result=self.db.query("select * from users4")
        for row in result:
            print(row)

    def get_user_by_id(self,id):
        sql="select * from users4 where id=%s"
        result=self.db.query(sql,(id,))
        if result:
            for row in result:
                print(row)

    def update_user_phone(self,id,new_phone):
        sql="update users4 set phone=%s where id=%s"
        self.db.execute(sql,(new_phone,id))
        result=self.db.query("select * from users4 where id=%s",(id,))
        if result:
            for row in result:
                print(row)


    def delete_user(self,id):
        sql="delete from users4 where id=%s"
        self.db.execute(sql,(id,))
        result=self.db.query("select * from users4")
        if result:
            for row in result:
                print(row)



if __name__ == '__main__':
    '''db = DBHelper('localhost','root','1234','company2')
    sql_update = "update users4 set phone=%s where username=%s"
    db.execute(sql_update, ('888', '张三'))
    users=db.query('select * from users4')
    if users:
        for row in users:
            print(row)
    db.close()'''
    db=DBHelper('localhost','root','1234','company2')
    user_manager=UserManager(db)

    try:
        #user_manager.add_user('小明','男','1560')
        user_manager.get_user_by_id(3)
        #user_manager.update_user_phone(2,666)
        #user_manager.delete_user(1)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        db.close()













