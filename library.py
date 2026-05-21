class Book:
    def __init__(self,title,author,price):
        self.title=title
        self.author=author
        self.price=price

    def show_info(self):
        print(f'书名:{self.title},作者:{self.author},价格:{self.price}元')

print('作业1:图书类')
book1=Book('Python编程','张三',59.9)
book1.show_info()
book2=Book('数据结构','李四',45.0)
book2.show_info()