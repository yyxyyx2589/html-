'''import requests
resp=requests.get('https://httpbin.org/get')
print('类型(text):',type(resp.text))
data=resp.json()
print('类型(json)',type(data))
'''

'''# 响应状态码实现异常检测
import requests
resp=requests.get('https://httpbin.org/status/400')
print('状态码:',resp.status_code)
try:
    resp.raise_for_status() #   检查HTTP请求是否出错
except requests.HTTPError as e:
    print('请求出错',e)
'''

''' #   捕获超时异常
import requests
try:
    r=requests.get('https://httpbin.org/delay/2',timeout=3)
    r.raise_for_status()
    print('请求成功')
except requests.exceptions.Timeout:
    print('请求超时,网络连接错误')
except requests.exceptions.RequestException as e: # RequestExceptio可捕获所有请求相关错误
    print('未知错误',e)'''

'''import requests
try:
    resp=requests.get('https://httpbin.org/ip',timeout=1)
    print('状态码:',resp.status_code)
    if resp.status_code==200:
        print("请求成功")
    else:
        print("请求失败")
    data=resp.json()
    print("解析为json格式：",data)
    print("IP地址为:",data['origin'])
except requests.exceptions.Timeout:
    print('请求超时,网络连接错误')
except requests.exceptions.RequestException as e:
    print('未知错误',e)
'''


'''def get_weather():
    if not city:
        print("请输入城市：")
    if not se.research()
    '''

'''import requests
base_all=0
url='https://restapi.amap.com/v3/weather/weatherInfo'
params_base={
    'city':'新余',
    'key':'7197563b3bb5d59cd1e2cf3c88965600',
    'extensions':'base',
    'output':'json'
}

print('请选择查询地点:')
pisition=input()
params_base['city']=pisition

print('请选择查询模式:1:今日天气 2:预测近三日天气')
x=int(input())
if x==1:
    resp = requests.get(url, params=params_base)
    resp_json=resp.json()
    data=resp_json['lives']
    print('province:',data[0]['province'])
    print('city:', data[0]['city'])
    print('adcode:', data[0]['adcode'])
    print('weather:', data[0]['weather'])
    print('temperature:', data[0]['temperature'])
    print('winddirection:', data[0]['winddirection'])
    print('windpower:', data[0]['windpower'])
    print('humidity:', data[0]['humidity'])
    print('reporttime:', data[0]['reporttime'])
    print('temperature_float:', data[0]['temperature_float'])
    print('humidity_float:', data[0]['humidity_float'])

if x==2:
    params_base['extensions']='all'
    resp = requests.get(url, params=params_base)
    resp_json = resp.json()
    data = resp_json['forecasts']
    print('province:', data[0]['province'])
    print('city:', data[0]['city'])
    print('adcode:', data[0]['adcode'])
    print('reporttime:', data[0]['reporttime'])
    fore=data[0]['casts']
    print(fore)
    for i in fore[0]:
        print(i)
        print(f'date:', fore[0]['date'], end=' ')
        print('dayweather:', fore[0]['dayweather'], end=' ')
        print('nightweather:', fore[0]['nightweather'], end=' ')
        print('daytemp:', fore[0]['daytemp'], end=' ')
        print('nighttemp:', fore[0]['nighttemp'], end=' ')
'''

'''class Student:
    school='新余学院'
    def study(self):
        print(f'{self.name}正在学习')

    def get_name1(self,name):
        self.name=name
        return self.name

student1=Student()
student2=Student()
student1.name,student2.name='张三','李四'
print(student1.school)
print(student2.study())
s=Student()
print(s.get_name1('李四'))'''


'''class Car:
    color='白色'
    def run(self):
        print(f'一辆{self.color}的车正在行驶')

car1=Car()
car2=Car()
car2.color='红色'
car1.run()
car2.run()'''


'''class Student:
    school='新余学院'
    def __init__(self,name,gender):
        self.name=name
        self.gender=gender

s1=Student('张三','男')
s2=Student('李四','女')
print(s1.name,s2.name)

print(s1.school)
print(Student.school)

Student.school='九江学院'
print(s1.school,s2.school)

print(s1.gender,s2.gender)
'''

'''class Rectangle:
    def __init__(self,width,height):
        self.width=width
        self.height=height

    def get_area(self):
        return self.width*self.height

    def get_perimeter(self):
        return 2*(self.width+self.height)

    @classmethod
    def create_square(cls,side):
        cls.side=side
        return cls(side,side)


q1=Rectangle(10,20)
print('矩形面积:',q1.get_area())
print('矩形周长:',q1.get_perimeter())
q2=Rectangle.create_square(4)
print('正方形面积:',q2.get_area())
print('正方形周长:',q2.get_perimeter())
'''


'''class Person:
    def __init__(self,name,age):
        self.name=name
        self.__age=age
    def get_age(self):
        return self.__age
    def set_age(self,age):
        if 0<=age<150:
            self.__age=age
            print("合法,年龄为:",self.__age)
        else:
            print("年龄不合法")

p=Person('张三','20')
p.set_age(160)
print(p.get_age())'''

'''
class Shape:
    def get_area(self):
        return 0

class Square(Shape):
    def __init__(self,side):
        self.side=side
    def get_area(self):
        return self.side*self.side

class Circle(Shape):
    def __init__(self,radius):
        self.radius=radius
    def get_area(self):
        return 3.14*self.radius*self.radius

def calculate_total_area(shape):
    total_area=0
    for shape in shape:
        total_area+=shape.get_area()
    return total_area

q1=Square(4)
q2=Circle(3)
li=[q1,q2]
print('总面积:',calculate_total_area(li))
'''


class BankAccount:
    def __init__(self,account_id,name,initial_balance=0000,password=0000):
        self.account_id=account_id
        self.name=name
        self.__balance=initial_balance
        self.__password=password
        print(f'账户{self.account_id}创建成功,用户名:{self.name}')

    def show_balance(self):
        print('账户余额:',self.__balance)
        return self.__balance

    def deposit(self,amount):
        print('请输入需要存储的金额:')
        if amount>0:
            self.__balance+=amount
            print(f"存款成功,存入{amount}元")
            print(self.show_balance())
        else:
            print("请输入正确数字")

    def withdraw(self,amount,password):
        if password!=self.__password:
            print("密码错误")
        if amount>self.__balance:
            print("取款失败，余额不足")
        elif amount<0:
            print("请输入正确数字")

        if password==self.__password:
            self.__balance-=amount
            print(f"取款成功，已取出{amount}元,余额:{self.__balance}")

    def transfer(self,password):
        if password!=self.__password:
            print("密码错误，请重新输入")
        if password==self.__password:
            print("密码正确，请输入新密码:")
            new_password=input()
            self.__password=new_password
            print("修改成功")

q1=BankAccount(123466,'张三',9999,0000)
q1.show_balance()
q1.deposit(100)
q1.withdraw(100,0000)
q1.transfer(0000)

