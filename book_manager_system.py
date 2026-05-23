import pymysql
import time
from datetime import datetime, timedelta

class Book_Manager:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="1234",
                database="book_db",
                charset="utf8mb4",
                autocommit=False
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            print("✅ 数据库连接成功")
        except Exception as e:
            print("❌ 数据库连接失败：", e)

    def super_admin(self,account):
        bm=Book_Manager()
        while True:
            print("\n============== 超级管理员界面 ==============")
            print("1. 添加管理员账号")
            print("2. 删除管理员账号")
            print("3. 查看所有管理员账号")
            print("4. 进入图书管理系统")
            print("5. 修改管理员密码")
            print("0. 退出系统")
            choice = input("请输入功能编号：")
            if choice == "1":
                account = input("输入账号(至少4位)：")
                password = input("输入密码(至少4位)：")
                bm.register_admin(account, password)

            elif choice == "2":
                account = input("输入账号：")
                password = input("输入密码：")
                bm.delete_admin(account, password)

            elif choice == "3":
                bm.show_all_manager(account)

            elif choice == "4":
                function_admin(account)

            elif choice == "5":
                account = input("输入账号：")
                password = input("修改后的密码(至少4位)：")
                bm.alter_admin(account,password)

            elif choice == "0":
                bm.close()
                bm.write_log(f"超级管理员{account}登出")
                print("✅ 退出成功！")
                break

            else:
                print("❌ 输入无效，请输入0-3的数字！")

    def show_all_manager(self, account):
        sql = "select * from admin"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            print(f"编号{row['admin_id']}, 账号{row['account']}, 密码{row['password']}")

    def delete_admin(self, account, password):
        try:
            sql="delete from admin WHERE account=%s"
            self.cursor.execute(sql, (account,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("✅ 删除管理员信息成功!")
                self.write_log(f"管理员账号:{account}已删除")
            else:
                print("❌ 未找到该管理员账号!")
        except Exception as e:
            print("❌ 删除异常！")

    def register_admin(self,account,password):
        try:

            sql = "select account from admin where account = %s"
            self.cursor.execute(sql, (account,))
            result = self.cursor.fetchone()

            if result is None:
                if len(account)>=4 and len(password)>=4:

                    sql = "insert into admin(account,password) values(%s,%s)"
                    self.cursor.execute(sql, (account, password))
                    self.conn.commit()
                    print("✅ 管理员注册成功!")
                    function_admin(account)
                    self.write_log(f"管理员{account}注册")
                else:
                    print("❌ 账号或密码少于4位，请重新输入！")
            else:
                print("❌ 该账号已被注册!")

        except Exception as e:
            self.conn.rollback()
            print(account,password)
            print(len(account),len(password))
            print("❌ 注册失败!")

    def register_stu(self, account, password):
        try:
            if account == "admin":
                print("❌ 该用户名无法注册！请重新注册！")
                return
            sql = "select account from student where account = %s"
            self.cursor.execute(sql, (account,))
            result = self.cursor.fetchone()

            if result is None:
                if len(account) >= 4 and len(password) >= 4:

                    sql = "insert into student(account,password) values(%s,%s)"
                    self.cursor.execute(sql, (account, password))
                    self.conn.commit()
                    print("✅ 学生用户注册成功!")
                    function_stu(account)
                    self.write_log(f"学生用户{account}注册")
                else:
                    print("❌ 账号或密码少于4位，请重新输入！")
            else:
                print("❌ 该账号已被注册!")

        except Exception as e:
            self.conn.rollback()
            print(account, password)
            print(len(account), len(password))
            print("❌ 注册失败!")


    def login(self,account,password):
        try:
            sql = "select password from admin where account = %s"
            self.cursor.execute(sql, (account,))
            result = self.cursor.fetchone()

            sql = "select password from student where account = %s"
            self.cursor.execute(sql, (account,))
            result2 = self.cursor.fetchone()

            if result is not None and account=='admin' and password==result['password']:
                print("✅ 超级管理员登录成功！")
                self.write_log(f"超级管理员{account}登录")
                self.super_admin(account)

            elif result is not None and password == result['password']:
                print("✅ 管理员登录成功!")
                function_admin(account)
                self.write_log(f"管理员{account}登录")

            elif result2 is not None and password == result2['password']:
                print("✅ 学生用户登录成功！")
                function_stu(account)
                self.write_log(f"学生用户{account}登录")

            else:
                print("❌ 用户不存在或密码错误!")

        except Exception as e:
            self.conn.rollback()
            print("❌ 登录失败!")

    def alter_admin(self,account,password):
        try:
            if account=='admin':
                print("❌ 无法修改此账号密码!")
            else:
                sql="select password from admin where account = %s"
                sql = "update admin set password = %s where account = %s"
                self.cursor.execute(sql, (password,account))
                self.conn.commit()
                if self.cursor.rowcount > 0:
                    print("✅ 修改密码成功!")
                    self.write_log(f"管理员账号:{account}密码修改成功")
                    return
                else:
                    print("❌ 修改失败,账号错误!")
                    return
        except Exception as e:
            print("❌ 修改失败！")
            self.conn.rollback()

    def alter_stu(self,account,password):
        try:
            sql="select password from student where account = %s"
            self.cursor.execute(sql, (account,))
            result = self.cursor.fetchone()

            if result is not None and password == result['password']:
                password = input("请输入新密码(至少4位):")
                if len(password) >= 4:
                    sql = "update student set password = %s where account = %s"
                    self.cursor.execute(sql, (password,account))
                    self.conn.commit()
                    print("✅ 修改密码成功!")
                    self.write_log(f"学生账号:{account}密码修改成功")
                else:
                    print("❌ 请重新输入！密码至少4位！")
            else:
                if result is None:
                    print("❌ 用户不存在！")
                else:
                    print("❌ 密码错误！")
        except Exception as e:
            print("❌ 修改失败！")
            self.conn.rollback()

    def add_book(self, book_id,book_name,author,category,status):
        try:
            sql="insert into book(book_id,book_name,author,category,status) values(%s,%s,%s,%s,%s)"
            self.cursor.execute(sql,(book_id,book_name,author,category,status))
            self.conn.commit()
            print("✅ 图书信息添加成功!")
            self.write_log(f"图书编号:{book_id}  书名:《{book_name}》 已添加")
        except Exception as e:
            self.conn.rollback()
            print("❌ 添加失败！请输入正确的图书编号或状态!")

    def select_all_book(self):
        sql="select * from book"
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        if not result:
            print("❌ 暂无图书信息")
            return
        print("============== 所有图书信息 ==============")
        for row in result:
            print(f"图书编号:{row['book_id']}     书名:《{row['book_name']}》     作者:{row['author']}     图书分类:{row['category']}     图书状态:{row['status']}")

    def select_book_by_id(self, book_id):
        sql="select * from book where book_id=%s"
        self.cursor.execute(sql,(book_id,))
        result=self.cursor.fetchone()
        if not result:
            print("❌ 查询不到该图书信息,请重新查询!")
            return
        print(f"============== 图书信息如下 ==============")
        print(f"图书编号：{result['book_id']}     书名：《{result['book_name']}》     作者:{result['author']}     图书分类:{result['category']}     图书状态:{result['status']}")

    def update_book(self, book_id, book_name, author, category):
        try:
            sql="update book set book_name=%s,author=%s,category=%s where book_id=%s"
            self.cursor.execute(sql,(book_name,author,category,book_id))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print("✅ 修改图书信息成功!")
                self.write_log(f"图书编号:{book_id}  书名:《{book_name}》 信息已修改")
            else:
                print("❌ 未找到该图书，图书编号不存在!")

        except Exception as e:
            self.conn.rollback()
            print("❌ 修改失败，请输入正确的图书编号!")


    def delete_book(self, book_id):
        try:
            x=input("是否确认删除该图书,删除后无法恢复！(yes/no)")
            if x == "yes":
                sql="delete from book where book_id=%s"
                self.cursor.execute(sql,(book_id,))
                result = self.cursor.fetchone()
                self.conn.commit()

                if self.cursor.rowcount > 0:
                    print("✅ 删除图书信息成功!")
                    self.write_log(f"图书编号:{book_id}  书名:《{result['book_name']}》 已删除")
                else:
                    print("❌ 未找到该图书,图书编号不存在!")

            elif x == "no":
                print("已返回上一步")
                self.conn.rollback()
            else:
                print("❌ 输入错误！请重新操作！")
                self.conn.rollback()

        except Exception as e:
            self.conn.rollback()
            print("❌ 删除失败,请输入正确的图书编号!")


    def borrow_book(self, book_id,account):
        try:
            sql="select * from book where book_id=%s"
            self.cursor.execute(sql,(book_id,))
            result=self.cursor.fetchone()
            if not result:
                print("❌ 图书编号不存在！")
                return

            if result['status']=="可借阅":
                sql="update book set status=%s where book_id=%s"
                self.cursor.execute(sql,('已借出',book_id))
                self.conn.commit()

                print("✅ 借阅成功")
                borrow_time=datetime.now()
                return_time = borrow_time+ timedelta(days=7)
                borrow_str = borrow_time.strftime("%Y-%m-%d %H:%M:%S")
                return_str = return_time.strftime("%Y-%m-%d %H:%M:%S")

                print(f"当前用户id:{account}  借阅图书编号:{book_id}  借阅日期:{borrow_str}  请于:{return_str}前归还")
                self.write_log(f"图书编号:{book_id}  书名:《{result['book_name']}》 已借出")
                return

            elif result['status']=="已借出":
                print("❌ 该本图书已借出")
        except Exception as e:
            print("❌ 图书编号不存在或操作失败！")

    def return_book(self, book_id):
        try:
            sql="select * from book where book_id=%s"
            self.cursor.execute(sql,(book_id,))
            result=self.cursor.fetchone()

            if not result:
                print("❌ 图书编号不存在！")
                return

            if result['status']=="已借出":
                sql="update book set status=%s where book_id=%s"
                self.cursor.execute(sql,('可借阅',book_id))
                self.conn.commit()
                print("✅ 还书成功!")
                self.write_log(f"图书编号:{book_id}  书名:《{result['book_name']}》 已归还")
            elif result['status']=="可借阅":

                print("❌ 该本图书未被借阅或已归还，不可还书!")

        except Exception as e:
            print("❌ 图书编号不存在或操作失败！")


    def fuzzy_select(self,book_name):
        sql="select * from book where book_name like %s"
        self.cursor.execute(sql,(f"%{book_name}%",))
        result = self.cursor.fetchall()

        if not result:
            print("❌ 查询不到该图书信息,请重新查询!")
            return
        print("============== 图书信息如下 ==============")
        for row in result:
            print(f"图书编号:{row['book_id']}     书名:《{row['book_name']}》     作者:{row['author']}     图书分类:{row['category']}     图书状态:{row['status']}")


    def category_select(self,category):
        sql="select * from book where category = %s"
        self.cursor.execute(sql,(category,))
        result=self.cursor.fetchall()

        if not result:
            print("❌ 该分类不存在图书!请重新查询！")
            return
        print(f"============== 图书信息如下 ==============")
        for row in result:
            print(f"图书编号:{row['book_id']}     书名:《{row['book_name']}》     作者:{row['author']}     图书分类:{row['category']}     图书状态:{row['status']}")

    def author_select(self,author):
        sql="select * from book where author = %s"
        self.cursor.execute(sql,(author,))
        result=self.cursor.fetchall()

        if not result:
            print("❌ 不存在该作者!请重新查询！")
            return
        print(f"============== 图书信息如下 ==============")
        for row in result:
            print(
                f"图书编号:{row['book_id']}     书名:《{row['book_name']}》     作者:{row['author']}     图书分类:{row['category']}     图书状态:{row['status']}")


    def close(self):
        self.conn.close()
        self.cursor.close()
        print("✅ 已关闭连接!")

    def write_log(self,msg):
        now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open("book_log.txt","a",encoding="utf-8") as f:
            f.write(f"{now}  {msg}\n")

def main():
    bm= Book_Manager()
    while True:
        print("\n============== 图书信息管理登录界面 ==============")
        print("1. 登陆账号")
        print("2. 注册账号")
        print("3. 修改密码")
        print("0. 退出系统")
        choice = input("请输入功能编号：")
        if choice == "1":
            account = input("输入账号：")
            password = input("输入密码：")
            bm.login(account, password)

        elif choice == "2":
            account = input("输入账号(至少4位)：")
            password = input("输入密码(至少4位)：")
            bm.register_stu(account, password)

        elif choice == "3":
            account = input("输入账号：")
            password = input("输入旧密码：")
            bm.alter_stu(account, password)

        elif choice == "0":
            bm.close()
            bm.write_log(f"用户{account}登出")
            print("✅ 退出成功，再见！")
            break

        else:
            print("❌ 输入无效，请输入0-3的数字！")


def function_admin(account):
    bm= Book_Manager()
    while True:
        print("\n============== 图书信息管理系统 ==============")
        print("1. 添加图书")
        print("2. 查询所有图书")
        print("3. 按图书编号查询")
        print("4. 修改图书信息")
        print("5. 删除图书")
        print("6. 借阅图书")
        print("7. 归还图书")
        print("8. 模糊查询图书")
        print("9. 分类查询图书")
        print("10. 作者查询图书")
        print("0. 退出系统")
        print("==========================================")

        choice = input("请输入功能编号：")

        if choice == "1":
            book_id = input("请输入图书编号：")
            book_name = input("请输入书名：")
            author = input("请输入作者：")
            category = input("请输入图书分类：")
            status = input("请输入图书状态：")
            bm.add_book(book_id, book_name, author, category,status)

        elif choice == "2":
            bm.select_all_book()

        elif choice == "3":
            book_id = input("请输入查询图书编号：")
            bm.select_book_by_id(book_id)

        elif choice == "4":
            book_id = input("请输入要修改的图书编号：")
            book_name = input("请输入新书名：")
            author = input("请输入新作者：")
            category = input("请输入新分类：")
            bm.update_book(book_id,book_name,author,category)

        elif choice == "5":
            book_id = input("请输入要删除图书的编号：")
            bm.delete_book(book_id)

        elif choice == "6":
            book_id = input("请输入要借阅图书的编号：")
            bm.borrow_book(book_id,account)

        elif choice == "7":
            book_id = input("请输入要归还图书的编号：")
            bm.return_book(book_id)

        elif choice == "8":
            book_name = input("请输入要查询图书的名字：")
            bm.fuzzy_select(book_name)

        elif choice == "9":
            category = input("请输入要查询的图书分类：")
            bm.category_select(category)

        elif choice == "10":
            author = input("请输入要查询的作者：")
            bm.author_select(author)

        elif choice == "0":
            print("✅ 系统退出成功！")
            break

        else:
            print("❌ 输入无效，请输入0-10的数字！")


def function_stu(account):
    bm= Book_Manager()
    while True:
        print("\n============== 图书信息借阅系统 ==============")
        print("1. 查询所有图书")
        print("2. 借阅图书")
        print("3. 归还图书")
        print("4. 模糊查询图书")
        print("5. 分类查询图书")
        print("6. 作者查询图书")
        print("0. 退出系统")
        print("==========================================")

        choice = input("请输入功能编号：")

        if choice == "1":
            bm.select_all_book()

        elif choice == "2":
            book_id = input("请输入要借阅图书的编号：")
            bm.borrow_book(book_id,account)

        elif choice == "3":
            book_id = input("请输入要归还图书的编号：")
            bm.return_book(book_id)

        elif choice == "4":
            book_name = input("请输入要查询图书的名字：")
            bm.fuzzy_select(book_name)

        elif choice == "5":
            category = input("请输入要查询的图书分类：")
            bm.category_select(category)

        elif choice == "6":
            author = input("请输入要查询的作者：")
            bm.author_select(author)

        elif choice == "0":
            print("✅ 系统退出成功！")
            break

        else:
            print("❌ 输入无效，请输入0-6的数字！ ")

if __name__ == "__main__":
    main()







