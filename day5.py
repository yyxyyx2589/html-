import os
'''
#   os.walk 返回一个元组，包含三个元素: 所有目录路径名，所有目录的列表，所有文件的列表
list_dirs=os.walk(os.getcwd())
for i,j,k in list_dirs:
    print(i,j,k)
'''

'''#   统计指定文件夹大小 以及文件和子文件夹数量
dirname=input() #文件夹 = 目录
totalsize,filenum,dirnum=0,0,0
if os.path.exists(dirname):

    for root, dirs, files in os.walk(dirname):
        print(root,dirs,files)
        dirnum+=len(dirs)
        filenum+=len(files)
        for file in files:
            filepath=os.path.join(root,file)
            totalsize+=os.path.getsize(filepath)
    totalsize=totalsize/1024/1024
    print(f"所有文件大小合为：{totalsize:.2f}MB，所有目录数量为：{dirnum}，所有文件数量为：{filenum}")
else:
    print("error")
    '''
'''
class Shortinputexception(Exception):
    def __init__(self,length,atleast):
        Exception.__init__(self)
        self.length=length
        self.atleast=atleast
try:
    s=input("请输入：")
    if len(s)<3:
        raise Shortinputexception(len(s),3)
except EOFError:
    print("你输入了一个结束标记EOF")
except Shortinputexception as x:
    print("short:长度是 %d ,至少应是 %d,"%(x.length,x.atleast))
else:
    print("没有异常")
'''
'''li=[]
# try except
while True:
    x=input("输入:")
    try:
        x=int(x)
        li.append(x)
        print("已输入{}".format(x))
    except Exception as e:
        print("error")
        print(li)'''


'''
try:
    x=input("输入成绩0-100:\n")
    if not x:
        raise ValueError("输入不能为空")
    x = float(x)
    if x<=0 or x>=100:
        raise ValueError("请输入0-100的数字")
except ValueError as e:
    print(f"error:{e}")
else:
    print("成绩输入成功:{}".format(x))
'''

'''import caculater as a
print(a.caculate())
'''


'''
from datetime import datetime
def show_time():
    now=datetime.now()
    ftm1=now.strftime("%Y年%m月%d日%H时%M分%S秒")
    ftm2=now.strftime("%A-%B-%d-%Y")
    print(ftm1,ftm2)

import random
import string
def suiji():
    cha=string.ascii_uppercase
    dig=string.digits
    num=cha+dig
    c=''.join(random.choices(num,k=6))
    print(c)'''


import json
'''data={'name':'李四','age':18}
json_str=json.dumps(data,ensure_ascii=True,indent=0)
print("转换后的json字符串:\n",json_str)
parsed_dict=json.loads(json_str)
print("\n提取姓名:",parsed_dict['name'])
print("提取年龄:",parsed_dict['age'])'''

dict={
"company": "Alibaba",
"employees": [{"name": "Alice", "position": "Engineer", "salary": 10000},
              {"name": "Bob", "position": "Manager", "salary": 15000}],
"location": "Hangzhou"}
json_str=json.dumps(dict,ensure_ascii=True,indent=0)
parsed_dict=json.loads(json_str)
print('公司名:',parsed_dict['company'])
print('地址:',parsed_dict['location'])

num=0
for i in parsed_dict['employees']:
        print('姓名:',i['name'],'职位:',i['position'])
        num+=i['salary']
ave=num/len(parsed_dict['employees'])
print('平均工资:',ave)

