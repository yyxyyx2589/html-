"""     index
n='aabbacc'
print(n.rfind('a'))
print(n.rindex('a'))
print(n.count('a'))
"""

"""     count
text='''aaabcdddabcd'''
for i,j in enumerate(text):
    if i == text.index(j):
        print((i,j,text.count(j)),end='')
     """

"""     solit   partition
text='''aaabcdddabcda'''
print(text.split('a'))
print(text.rsplit('a'))
print(text.partition('a'))
print(text.rpartition('x'))
print(text.rpartition('a'))
"""

'''     替换
table=''.maketrans('abcdef','123456')
text='this is a computer'
print(text.translate(table))

words=('you','i','co')
text='this is a computer'
for i in words:
    if i in text:
        print(text.replace(i,'***'))'''

'''
text='i go to school tomorrow.'
count=0
for ele in text:
    if ele in [',','.']:
        print("1")
        text.replace(ele,'!')
        print(text)
    if ele==' ':
        count+=1
print(text)
print(f"有{count}个单词")'''


'''     封装
text='hello world!I like python.this is a nice day.right?'
count=0

#   转成大写/小写
def trans():
    print(text.lower())
    print(text.upper())
"""for ele in text:
    li.append(ele)
    if ele in [',','.','!','?']:
        """
# 统计个数
def count_():
    global count
    for ele in text:
        if ele in [',','.','!','?',' ']:
            count+=1
    print('单词个数为:',count)

#   加密
def jiami():
    print("加密多少位")
    k=int(input())
    lower_letter='abcdefghijklmnopqrstuvwxyz'
    upper_letter='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_letter_k=lower_letter[k:]+lower_letter[:k]
    upper_letter_k=upper_letter[k:]+upper_letter[:k]
    table=''.maketrans(lower_letter+upper_letter,lower_letter_k+upper_letter_k)
    print(text.translate(table))

if __name__=='__main__':
    while True:
        print("输入要执行的操作")
        print("1:转换大小写")
        print("2:统计单词个数")
        print("3:加密k位")
        n = int(input())
        if n == 1:
            trans()
        if n == 2:
            count_()
        if n == 3:
            jiami()
        if n == 4:
            break'''

#       strip
'''text=('abcdabcdaab')
print(text.strip('ab'))
print(text.rstrip('ab'))
print(text.lstrip('ab'))'''

#   文本规范化
"""
text='''姓名:张三
年龄:39
性别:男
性取向:男'''

inf=text.split("\n")    #split  删除(以此为界限)
print(inf)
for i in inf:                       #sep 本来默认是空格，现在是:和空格
    print(i[:2],i[2:].strip(': '),sep=': ')     #strip  把（）去掉
"""


'''print(string.digits)
print(string.ascii_uppercase)
print(string.ascii_lowercase)
print(string.punctuation)
print(string.whitespace)'''

'''
import string
cha=string.ascii_letters
import random
print("输入密码位数")
x=int(input())
print(random.choice(string.punctuation) + ''.join([random.choice(cha) for i in range(x-1)]))
'''

# 文件
'''s='hello world\n'
p='sdjfhnewuf'
with open('test.txt','w') as fp:
    fp.write(s)
    fp.write(p)
with open('test.txt') as fp:
    print(fp.read())

with open('test.txt','r') as fp:
    d=fp.read(5)
print(d)
print(len(d))

with open('test.txt') as fp:
    for line in fp:
        print(line,end='')'''

'''
def write_():
    with open('test.txt', 'w') as fp:
        while True:
            print("输入数字：(输入no结束)")
            ele = input()
            if ele == 'no':
                break
            else:
                fp.write(ele+'\n')


def pai_xu():
    li=[]
    with open('test.txt', 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            li.append(int(line.strip()))
    li.sort()
    print(li)
    with open('test.txt', 'w') as fp:
        for i in li:
            fp.write(str(i)+'\n')
            print(i)

def main():
    while True:
        print("您想进行什么操作")
        print("1:写入")
        print("2:排序")
        print("3:退出")
        n = int(input())
        if n == 1:
            write_()
        if n == 2:
            pai_xu()
        if n == 3:
            break

main()'''


import os
print([fname for fname in os.listdir(os.getcwd())if os.path.isfile(fname) and fname.endswith('.py')])
'''
# 1. 获取当前目录下的所有文件和文件夹名称
all_names = os.listdir(os.getcwd())
# 2. 准备一个空列表，用来存放符合条件的 .py 文件
py_files = []
# 3. 逐个检查每一个名字
for fname in all_names:
    # 判断它是不是一个文件（而不是文件夹）
    is_file = os.path.isfile(fname)
    # 判断它的名字是不是以 .py 结尾
    is_py = fname.endswith('.py')
    # 如果两个条件都满足，就把它加到列表里
    if is_file and is_py:
        py_files.append(fname)
print(py_files)
'''

'''count=0
p=os.getcwd()
all_names = os.listdir(p)
all_names2=[fname for fname in os.listdir(os.getcwd())if os.path.isfile(fname) and fname.endswith('.py')]
print(all_names)
print(all_names2)
for i in all_names2:
    if i.endswith('.py') and os.path.isfile(i):
        count+=1
if count==len(all_names2):
    print("yes")
else:
    print("no")'''


ml=input()
wjm=input()
file_path = os.path.join(ml,wjm)
if os.path.exists(file_path):
    print(file_path)
else:
    print("不存在")

#C:\Users\yyx\Desktop



