
#  map
"""
def pf(x):
    return x**2
print(list(map(pf,range(1,6))))
"""


#enumerate
"""
s=['香蕉','橙子','西瓜','葡萄']
print(s)
for index,value in enumerate(s):
    print((index,value),end='')
"""

"""
s=[]
for i in range(0,11):
    s.append(i)
print(s)

def ji(x):
        return x%2!=0

def ou(x):
        return x%2==0

print(filter(ji,s))
print(list(filter(ji,s)))
print(list(filter(ou,s)))
"""

#  filter
'''
s=[1,-2,3,-4,5,-6]
b=[]
def zheng(x):
    if x>0:
        b.append(x)
        return x

print(list(filter(zheng,s)))

def cheng2(x):
    return x*2

print(list(map(cheng2,b)))
'''

#  zip
'''
a=['张三','李四']
b=[50,60]
c=['男','女']
n=m=0
d=list(zip(a,b,c))
print(d)
for i in b:
    n+=1
    if i>=60:
        print(d[n-1])
        m+=1
print("合格人数为：",m)
'''

#   lambda
"""
a=['a','b','c']
b=['语文','数学','英语']
d=[]

c1=[50,60,70]
c2=[80,90,100]
c3=[90,80,0]

b1=list(zip(b,c1))
b2=list(zip(b,c2))
b3=list(zip(b,c3))

b1.append('a')
b2.append('b')
b3.append('c')

print(b1)
print(b2)
print(b3)
#总分
d1=sum(c1)
d2=sum(c2)
d3=sum(c3)

def pjf(x):
    return lambda:x/3

#平均分
e1=pjf(d1)
e2=pjf(d2)
e3=pjf(d3)

def hege(e):
    if e<60:
        return("不合格")
    if 60<=e<85:
        return("合格")
    if 85<=e<100:
        return("优秀")
print(f"a的平均分：{e1():.2f}",hege(e1()))
print(f"b的平均分：{e2():.2f}",hege(e2()))
print(f"c的平均分：{e3():.2f}",hege(e3()))

for i in range(len(a)):
    print(b[i],"成绩最高的是",end='')
    max1=max(b1[i][1],b2[i][1],b3[i][1])
    if max1==b1[i][1]:
        print(b1[-1],max1)
    elif max1==b2[i][1]:
        print(b2[-1],max1)
    elif max1==b3[i][1]:
        print(b3[-1],max1)
"""


'''
print("请输入数字")
m=input()
try:
    m=float(m)
    if 90<=m<=100:
        print(f"该学生成绩为{m},等级为a")
    elif 80<=m<90:
        print(f"该学生成绩为{m},等级为b")
    elif 70<=m<80:
        print(f"该学生成绩为{m},等级为c")
    elif 60<=m<70:
        print(f"该学生成绩为{m},等级为d")
    elif 0<=m<60:
        print(f"该学生成绩为{m},等级为f")
    else:
        print("输入错误")
except ValueError:
    print("输入错误")
'''

"""
li=[]
while 1:
    print("是否输入下一个分数,yes or no")
    answer=input()
    if answer=='yes':
        print("请输入分数:",end='')
        try:
            x=int(input())
            li.append(x)
        except ValueError:
            print("输入错误")
    elif answer=='no':
        val=sum(li)/len(li)
        print("所有分数为:",li)
        print("平均分为:",val)
        break
"""


# 计算素数
"""
li=[]
for i in range(1,101):
    count=0
    for j in range(1,i+1):
        if i%j==0:
            count+=1
    if count==2:
        li.append(i)
print(li)
print("100以内的最大素数为:",max(li))
"""

#能被7不能被5整除
"""
for i in range(1,101):
    if i%7==0 and i%5!=0:
        print(i)
"""

# 水仙花数
"""
for i in range(100,1000):
    a=i%10
    c=i//100
    b=(i-100*c)//10
    if i==a**3+b**3+c**3:
        print(i)
  """

# n位水仙花数
"""
n=int(input())
for i in range(10**(n-1),10**n):
    sum=0
    k=str(i)
    for j in range(len(k)):
        sum+=int(k[j])**n
    if sum==i:
        print(i)
"""





