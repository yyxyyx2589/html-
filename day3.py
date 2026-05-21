"""
li=[1,2,3,4,5,6,7,8,9]
li2=[2,5,8]

#   增
li.append(11)       #append(元素)
print(li)
li.extend(li2)      #extend(容器)
print(li)
li.insert(2,6) #在下标为2的后面加上元素6   insert(下标，元素)
print(li)

#   删
li.remove(6)        #remove(元素)
print(li)
del li[2]         #del(下标)    移除下标为2的元素
print(li)
li.pop(5)            #pop(下标)
print(li)

#   改       列表[下标] = 新值
li[0]=666

#   查
print(li.index(8))   #index(元素)
print(li)
print(li.count(2))  #count(元素)
print(li)

#   排序 反转
li.sort()   #sort
print(li)
sorted(li)  #返回一个新列表
li.reverse()
print(li)

#   切片     列表[start:end:step]
print(li[2:6:1])        #下标 2 到 6 的元素组成一个新列表 步长为 1
li[3:5:1]=888
print(li)

"""


"""
li=[]
while 1:
    print("请输入内容")
    li.append(input())
    print("是否继续 y/n")
    answer=input()
    if answer=="y":
        continue
    if answer=="n":
        break

print(li)
li.reverse()
print(li)
print(li.count(li[1]))
"""

#   字典
"""
di=dict()
s = {'name': '小明', 'age': 18, 'city': '北京'}
print(s.items())
print(s.keys())
print(s.values())
print(s.get('name'))
del s['name']
print(s)
age=s.pop('age')
print(age)
"""


def gender_if():
    print("请输入要查询号码的学号")
    n=input()
    if n in st:
        print('号码为:',st[n].get('phone'))
        if st[n].get('gender')=='男':
            print("性别:男生")
        else:
            print("女生")


def del_id():
    print("请输入要删除的学号:")
    id=input()
    if id in st:
        del st[id]
    print("已删除")
    for i in st.items():
        print(i)

def update_id():
    print("输入要更新数据的学号")
    id=input()
    if id in st:
        st1=st[id]
    print("请输入要更新的数据名")
    ele=input()
    print("请输入修改后的内容")
    st1[ele]=input()
    print(st1)

"""st={'41':{'name':'yyx','age':'22','gender':'男','phone':'190'}}
st['42']= {'name':'za','age':'20','gender':'女','phone':'188'}
st['43']= {'name':'zc','age':'20','gender':'男','phone':'166'}
st['44']= {'name':'zcc','age':'20','gender':'女','phone':'199'}
st1={}"""

st1={}
def gender_search():
    print("请输入要筛选的性别")
    gen=input()
    for i,j in st.items():
        if j['gender'] == gen:
            print(st[i])

def show_all(st):
    print("目前所有信息")
    for i,j in st.items():
        id=i
        name=j['name']
        age=j['age']
        gender=j['gender']
        phone=j['phone']
        print(f"学号:{id},姓名:{name},年龄:{age},性别:{gender},号码:{phone}")

def add(st):
    print("请输入学号")
    id=input()
    st={id:{}}
    print("请输入姓名")
    name = input()
    st[id]['name'] = name
    print("请输入年龄")
    age = input()
    st[id]['age'] = age
    print("请输入性别")
    gender = input()
    st[id]['gender'] = gender
    print("请输入号码")
    phone = input()
    st[id]['phone'] = phone
    show_all(st)
    return st

def main():
    global st
    if st== {}:
        print("目前无任何信息，请添加")
        st=add(st)
        main()
    else:
        while True:
            print("您想进行什么操作")
            print("1:查找所有男/女生信息")
            print("2:更新信息")
            print("3:删除学号")
            print("4:查询号码及性别")
            print("5:显示所有信息")
            print("6:退出")
            n=int(input())
            if n==1:
                gender_search()
            if n==2:
                update_id()
            if n==3:
                del_id()
            if n==4:
                gender_if()
            if n==5:
                show_all(st)
            if n==6:
                break

if __name__ == '__main__':
    st = {}
    main()


"""
def demo(newitem,old_list=[]):
    old_list.append(newitem)
    return old_list
print(demo('5',[1,2,3,4]))
print(demo('aaa',['a','b']))
print(demo('a'))
print(demo('b'))
"""
