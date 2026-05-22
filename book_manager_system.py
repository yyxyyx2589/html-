import pymysql
import time

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

    def login(self,account,password):
        try:
            sql = "select password from admin where account = %s"
            self.cursor.execute(sql, (account,))
            result = self.cursor.fetchone()
            if password == result['password']:
                print("登录成功")
                self.write_log(f"用户{account}登录")
                function()
            else:
                print("密码错误")

        except Exception as e:
            self.conn.rollback()
            print("登录失败")


    def add_book(self, book_id,book_name,author,category,status):
        try:
            sql="insert into book(book_id,book_name,author,category,status) values(%s,%s,%s,%s,%s)"
            self.cursor.execute(sql,(book_id,book_name,author,category,status))

            self.conn.commit()
            print("图书信息添加成功!")
            self.write_log(f"图书编号:{book_id}  书名:《{book_name}》 已添加")
        except Exception as e:
            self.conn.rollback()
            print("添加失败！请输入正确的图书编号或状态!")

    def select_all_book(self):
            sql="select * from book"
            self.cursor.execute(sql)
            result=self.cursor.fetchall()
            if not result:
                print("暂无图书信息")
                return
            print("================所有图书信息================")
            self.write_log("查询所有图书信息")
            for row in result:
                print(f"图书编号:{row['book_id']}     书名:《{row['book_name']}》     作者:{row['author']}     图书分类:{row['category']}     图书状态:{row['status']}")

    def select_book_by_id(self, book_id):
        sql="select * from book where book_id=%s"
        self.cursor.execute(sql,(book_id,))
        result=self.cursor.fetchone()
        if not result:
            print("查询不到该图书信息,请重新查询")
            return
        self.write_log(f"通过编号查询图书   图书编号:{book_id}  书名:《{result['book_name']}》")
        print(f"=======图书信息如下=======")
        print(f"图书编号：{result['book_id']}")
        print(f"书名：《{result['book_name']}》")
        print(f"作者：{result['author']}")
        print(f"图书分类：{result['category']}")
        print(f"图书状态：{result['status']}")

    def update_book(self, book_id, book_name, author, category):
        try:
            sql="update book set book_name=%s,author=%s,category=%s where book_id=%s"
            self.cursor.execute(sql,(book_name,author,category,book_id))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("修改图书信息成功")
                self.write_log(f"图书编号:{book_id}  书名:《{book_name}》 已修改")
            else:
                print("未找到该图书，图书编号不存在")

        except Exception as e:
            self.conn.rollback()
            print("修改失败，请输入正确的图书编号")


    def delete_book(self, book_id):
        try:
            x=input("是否确认删除该图书,删除后无法恢复！(yes/no)")
            if x == "yes":
                sql="delete from book where book_id=%s"
                self.cursor.execute(sql,(book_id,))
                result = self.cursor.fetchone()
                self.conn.commit()
                if self.cursor.rowcount > 0:
                    print("删除图书信息成功")
                    self.write_log(f"图书编号:{book_id}  书名:《{result['book_name']}》 已删除")
                else:
                    print("未找到该图书,图书编号不存在")
            elif x == "no":
                print("已返回上一步")
                self.conn.rollback()
            else:
                print("输入错误！请重新操作！")
                self.conn.rollback()

        except Exception as e:
            self.conn.rollback()
            print("删除失败,请输入正确的图书编号")


    def borrow_book(self, book_id):
        try:
            sql="select * from book where book_id=%s"
            self.cursor.execute(sql,(book_id,))
            result=self.cursor.fetchone()
            if result['status']=="可借阅":
                sql="update book set status=%s where book_id=%s"
                self.cursor.execute(sql,('已借出',book_id))
                self.conn.commit()
                print("借阅成功")
                self.write_log(f"图书编号:{book_id}  书名:《{result['book_name']}》 已借出")
            elif result['status']=="已借出":
                print("该本图书已借出")
        except Exception as e:
            print("图书编号不存在！")

    def return_book(self, book_id):
        try:
            sql="select * from book where book_id=%s"
            self.cursor.execute(sql,(book_id,))
            result=self.cursor.fetchone()
            if result['status']=="已借出":
                sql="update book set status=%s where book_id=%s"
                self.cursor.execute(sql,('可借阅',book_id))
                self.conn.commit()
                print("还书成功")
                self.write_log(f"图书编号:{book_id}  书名:《{result['book_name']}》 已归还")
            elif result['status']=="可借阅":
                print("该本图书未被借阅或已归还，不可还书")
        except Exception as e:
            print("图书编号不存在！")

    def close(self):
        self.conn.close()
        self.cursor.close()
        print("已关闭连接!")

    def write_log(self,msg):
        now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open("book_log.txt","a",encoding="utf-8") as f:
            f.write(f"{now}  {msg}\n")

def main():
    bm= Book_Manager()
    while True:
        print("\n======= 图书信息管理登录界面 =======")
        print("1. 登陆账号")
        print("0. 退出系统")
        choice = input("请输入功能编号：")
        if choice == "1":
            account = input("输入账号：")
            password = input("输入密码：")
            bm.login(account, password)

        elif choice == "0":
            bm.close()
            bm.write_log(f"用户{account}登出")
            print("退出成功，再见！")
            break

        else:
            print("❌ 输入无效，请输入0-1的数字！")


def function():
    bm= Book_Manager()
    while True:
        print("\n======= 图书信息管理系统 =======")
        print("1. 添加图书")
        print("2. 查询所有图书")
        print("3. 按图书编号查询")
        print("4. 修改图书信息")
        print("5. 删除图书")
        print("6. 借阅图书")
        print("7. 归还图书")
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
            bm.borrow_book(book_id)

        elif choice == "7":
            book_id = input("请输入要归还图书的编号：")
            bm.return_book(book_id)

        elif choice == "0":
            print("系统退出成功！")
            break

        else:
            print("❌ 输入无效，请输入0-7的数字！")


if __name__ == "__main__":
    main()







