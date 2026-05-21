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
    db=DBHelper('localhost','root','1234','company2')
    user_manager=UserManager(db)
            #  之前创建的表的结构
    #create table if not exists users4(
     #   id int primary key auto_increment,
      #  username varchar(20) not null,
       # gender enum('男','女') default('男'),
        #phone varchar(20) not null)

    try:
        #user_manager.add_user('小明','男','1560')
        user_manager.get_user_by_id(3)
        #user_manager.update_user_phone(2,666)
        #user_manager.delete_user(1)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        db.close()
