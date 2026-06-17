import numpy as np
"""
li=[[[1,2,3],[4,5,6],[7,8,9]], [[1,2,3],[4,5,6],[7,8,9]]]
arr=np.array(li)
print(arr)
arr1=np.array([[1,2],[4,5]])
arr2=np.array([[7,8],[4,5]])
print(arr.ndim)
print(arr.size)
print(arr.dtype)
print(arr.shape)

print(np.zeros((2,3)))  #全0
print(np.ones((2,3)))   #全1
print(np.eye(2))    #单位矩阵
print(np.full((2,3),5)) #全5
print(np.arange(10,20,2))   #间隔2
print(np.linspace(10,20,3)) #三份
print(np.random.randint(0,3,size=(2,3)))   #范围0-3   大小2*3

print(arr.reshape(6,3))
transposed=arr.T
print(transposed)

print(np.concatenate((arr2,arr1)),0)


grades=np.array([[1,2,3],[4,5,6],[7,8,9]])
print(grades.mean())
print(grades.max())
print(grades.min())
print(grades.std())

print(grades.mean(axis=0))
print(grades.mean(axis=1))

"""

"""arr=np.random.randint(0,100,size=(2,5,3))   #0:2班 1:5人 2:3科
print(arr)
print("每个班平均成绩",arr.mean(axis=(1,2)))
print("每个班每门课平均成绩",arr.mean(axis=1))
print("每门课中位数",np.median(arr,axis=(0,1)))
print("每个学生最高分",arr.max(axis=2))
print("每个学生最低分",arr.min(axis=2))"""



"""arr=np.array([[1,2,3],[4,5,6],[7,8,9]])
print(arr[1,2])
print(arr[:,1])
print(arr[:2,2])"""


"""
arr1=np.random.randint(0,100,size=(2,5,3))   #0:2班 1:5人 2:3科
print(arr1)

print("班级一",arr1[0])
print("所有班级第三个学生",arr1[:2,2])
print("最后一个班级，后两个学生",arr1[:-1,3:5])
print("所有班级最后一门课",arr1[:2,:5,2])"""


"""
grades=np.array([[1,2,3],[4,5,6],[7,8,9]])
mask=grades>=5
print(mask)
high_scores=grades[mask]
print(high_scores)

adj_grades=np.where(grades>=5,2,grades)
print(adj_grades)

indices=np.where(adj_grades>=2)
print(indices)"""




"""grades=np.random.randint(0,100,size=(2,5,3))   #0:2班 1:5人 2:3科
print(grades)
x=grades[0]
mask=x>85
high_scores=x[mask]
print("第一个班级大于85分:",high_scores)

b=np.where(grades>=90,'优秀',grades,)
print(b,'\n')
c=np.where(grades<=60,'不及格',grades)
print(c)


mask=grades<60
high_scores=grades[mask]
print("所有不及格成绩:",high_scores)"""



"""
arr_2d=np.array([[1,2,3],[4,5,6],[7,8,9]])
arr_1d=np.array([1,1,3])
arr_3d=np.array([[[1,2,3],[4,5,6],[7,8,9]],[[1,2,3],[4,5,6],[7,8,9]]])
print(arr_1d + arr_2d)
print(arr_1d + arr_3d)"""

"""
np.random.seed(42)
n=50
ids=np.arange(1,n+1)
math=np.clip(np.round(np.random.normal(75,15,n)),0,100).astype(int)
eng=np.clip(np.round(np.random.normal(78,11,n)),0,100).astype(int)
chin=np.clip(np.round(np.random.normal(80,10,n)),0,100).astype(int)

mec=np.column_stack((math,eng,chin))
sum=mec.sum(axis=1)
ave=mec.mean(axis=1)

student_data=np.column_stack((ids,math,eng,chin,sum,ave))
#print(student_data)"""
"""#   1.各科统计平均分   最高分 最低分
print(f"数学平均分：{np.mean(math)},数学最高分：{np.max(math)},数学最低分：{np.min(math)}")
print(f"英语平均分：{np.mean(eng)},英语最高分：{np.max(eng)},英语最低分：{np.min(eng)}")
print(f"语文平均分：{np.mean(chin)},语文最高分：{np.max(chin)},语文最低分：{np.min(chin)}")

#   2.每人总分  平均分

#   3.总分最高学生
mask=np.argmax(student_data[:,4])
print("总分最高学生：",student_data[mask])

#   4.挂科学生 任意一科小于60
mask=(mec<60).any(axis=1)
stu=student_data[mask]
print(stu)
print(stu.shape[0])

#   5.按总分排名
indices=np.argsort(student_data[:,4])
print(indices)

rank=student_data[indices]
print(rank)"""
"""
#   6.数学大于85    英语大于75
mask=(math>85)&(eng>75)
print(student_data[mask])


#   7.数据修改
current_math=student_data[:,1]
new_math=np.clip(current_math+5,0,100)
student_data[:,1]=new_math

#   8.统计分析
indices=np.argsort(-student_data[:,4])
rank=student_data[indices]
top10=rank[:10]
top_ave=top10[:,5]
print(top_ave)
"""


"""import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

plt.rcParams['font.sans-serif']=['SimHei']

x=np.linspace(0,10,100)
y1=np.sin(x)
y2=np.cos(x)


plt.figure(num=None,figsize=(10,10),dpi=80,facecolor='w',edgecolor='w')
plt.plot(x,y1,label='sin(x)',color='blue',linestyle='dashed')
plt.plot(x,y2,label='cos(x)',color='red',linestyle='dashed',linewidth=10,alpha=0.9,marker='*',ms=20,mfc='yellow',mec='blue',mew=1)


plt.title('测试')
plt.xlabel('x'),plt.ylabel('y')
plt.legend(),plt.grid(True,alpha=0.9)

plt.show()"""

"""plt.plot([1,2,3,4],[1,4,9,16],'go--')
plt.show()"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

plt.rcParams['font.sans-serif'] = ['SimHei']  #字体为黑体
plt.rcParams['axes.unicode_minus'] = False    #解决负号'-'显示为方块的问题

x = np.linspace(-2*np.pi,2*np.pi,200)

y1 = np.exp(x)      # y_1 = e^x
y2 = x**2           # y_2 = x^2
y3 = np.sin(3*x)    # y_3 = sin(3x)
y4 = np.cos(2*x)    # y_4 = cos(2x)

plt.figure(figsize=(10,6))

#每条曲线添加专属label标签
plt.plot(x,y1,color='#FF6B6B',linestyle='-',marker='o',markersize=4,label=r'$y_1 = e^x$')  # 红色实线圆形标记
plt.plot(x,y2,color='#4ECDC4',linestyle='--',marker='s',markersize=4,label=r'$y_2 = x^2$') # 青绿色虚线方形标记
plt.plot(x,y3,color='#45B7D1',linestyle='-.',marker='^',markersize=4,label=r'$y_3 = \sin(3x)$') # 蓝色点划线三角形标记
plt.plot(x,y4,color='#96CEB4',linestyle=':',marker='*',markersize=4,label=r'$y_4 = \cos(2x)$') # 绿色点线星形标记

plt.xlabel('X Axis',fontsize=12)
plt.ylabel('Y Axis',fontsize=12)
plt.title('四种函数曲线',fontsize=14)

#legend()展示图例，自定义摆放位置
plt.legend(loc='upper left',fontsize=10)

#网格线，设置网格为浅色虚线
plt.grid(True,linestyle='--',alpha=0.3)

#统一设置坐标轴字体、标题字体大小
plt.tick_params(axis='both',labelsize=10)

#限定x轴、y轴显示范围
plt.xlim(-5,5)
plt.ylim(-2,10)

plt.tight_layout()
plt.show()