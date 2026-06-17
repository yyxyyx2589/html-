import sklearn
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

from sklearn import metrics
from sklearn import preprocessing
from sklearn import model_selection
from sklearn import linear_model
from sklearn import datasets

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

plt.rcParams['font.sans-serif'] = ['SimHei']  #字体为黑体
plt.rcParams['axes.unicode_minus'] = False    #解决负号'-'显示为方块的问题

import warnings
warnings.filterwarnings('ignore')

import os
os.environ['PYTHONWARNINGS'] = 'ignore'

"""iris = load_iris()
x=iris.data
y=iris.target

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)

plt.figure(figsize=(10,6));colors=['red','blue','green']
for i,c in enumerate(colors):plt.scatter(x[y==i,0],x[y==i,2],c=c,label=iris.target_names[i],edgecolor='k',s=50)

plt.xlabel('sepal length')
plt.ylabel('Petal Length')
plt.title('iris dataset')
plt.legend()
plt.show()


pipe=make_pipeline(StandardScaler(),LogisticRegression())
pipe.fit(x_train,y_train)

y_pred=pipe.predict(x_test)
acc=accuracy_score(y_test,y_pred)
print(f"模型在测试机的准确率:{acc:.2f}")"""


# 有监督
"""#   不使用pipeline
iris = load_iris()
x=iris.data
y=iris.target

#   划分数据集
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)

scaler=StandardScaler()
scaler.fit(x_train)

x_train_scaled=scaler.transform(x_train)    #标准化
x_test_scaled=scaler.transform(x_test)    #标准化


model=LogisticRegression(max_iter=200,random_state=42)
model.fit(x_train_scaled,y_train)   #使用标准化后的训练数据

y_train_pred=model.predict(x_train_scaled)
y_pred=model.predict(x_test_scaled) #预测

train_acc=accuracy_score(y_train,y_train_pred)
acc=accuracy_score(y_test,y_pred)
print(f"模型在训练集的准确率:{train_acc:.2f}")
print(f"模型在测试集的准确率:{acc:.2f}")


plt.figure(figsize=(10,6));colors=['red','blue','green']
for i,c in enumerate(colors):plt.scatter(x[y==i,0],x[y==i,2],c=c,label=iris.target_names[i],edgecolor='k',s=50)

plt.xlabel('sepal length')
plt.ylabel('Petal Length')
plt.title('iris dataset')
plt.legend()
plt.show()"""

"""
import numpy as np
np.random.seed(42)
area=np.random.randint(50,150,size=100)
price=1.2*area+10+np.random.normal(0,10,size=100)

x=area.reshape(-1,1)
y=price
print("面积数据形状:",x.shape)
print("价格数据形状:",y.shape)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)
print(x_train.shape[0])
print(y_train.shape[0])

model=LinearRegression()
model.fit(x_train,y_train)
print(f"斜率m:{model.coef_[0]:.2f}")
print(f"截距b:{model.intercept_:.2f}")
y_pred = model.predict(x)

rf_model=RandomForestRegressor(n_estimators=100,random_state=42)
rf_model.fit(x_train,y_train)
y_pred=rf_model.predict(x)


plt.figure(figsize=(10,6))
plt.scatter(area,price,alpha=0.5,color='skyblue',label='Data Points')


plt.plot(area, y_pred, color='red', label='Fitted Line')

plt.xlabel('area (sq.m)')
plt.ylabel('price (10000 yuan')
plt.title('house dataset')
plt.legend()
plt.show()

"""

"""
#   1.加载数据
iris=load_iris()
x=iris.data

#   2.特征标准化
scaler=StandardScaler()
x_scaled=scaler.fit_transform(x)    #标准化之后  x_scaled

#   3.创建k-means聚类模型
kmeans=KMeans(n_clusters=5,random_state=42) #创建kmeand模型

#   4.模型训练
y_pred=kmeans.fit_predict(x_scaled) #训练后的样本标签

#   5.打印聚类中心
print("聚类中心点:")
print(kmeans.cluster_centers_)

#   6.可视化聚类结果
plt.scatter(x_scaled[:,0],x_scaled[:,1],c=y_pred,cmap='viridis')
#- c=y_pred ：根据 y_pred 的值为每个点分配颜色
#- 相同聚类标签的样本点会显示相同颜色
#- 不同聚类标签的样本点会显示不同颜色（通过 cmap='viridis' 配色方案）

centers=kmeans.cluster_centers_
plt.scatter(centers[:,0],centers[:,1],c='red',marker='*',s=200,label='聚类中心')
plt.title("kmeans无监督聚类结果")
plt.legend()
plt.show()
"""

import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score, mean_absolute_error

#   无监督
"""# 1.生成数据
x,y=make_regression(
    n_samples=500,
    n_features=3,
    noise=20,
    random_state=42
)

# 映射到真实范围
x[:,0]=np.interp(x[:,0],(x[:,0].min(),x[:,0].max()),(50,100))
x[:,1]=np.interp(x[:,1],(x[:,1].min(),x[:,1].max()),(0,30))
x[:,2]=np.interp(x[:,2],(x[:,2].min(),x[:,2].max()),(1,5))
x[:,2]=np.round(x[:,2]).astype(int)

y=np.interp(y,(y.min(),y.max()),(80,500))# 房价
y=np.round(y,2)

print("x shape:",x.shape)
print("y shape:",y.shape)
print("\n 前五行",x[:5])
print("\n 前五个房价",y[:5])

# 2.划分训练集
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

# 3.训练随机森林
model=RandomForestRegressor(n_estimators=100,random_state=42) # 决策树数量n_estimators
model.fit(x_train,y_train)
y_pred=model.predict(x_test)

print("\nR²",round(r2_score(y_test,y_pred),4))
print("MAE",round(mean_absolute_error(y_test,y_pred),2))

# 4.可视化
plt.rcParams['font.sans-serif'] = ['SimHei']  #字体为黑体
plt.rcParams['axes.unicode_minus'] = False    #解决负号'-'显示为方块的问题

# 图1 特征分布直方图 面积 房龄 房间数
plt.figure(figsize=(15,4))
titles=['面积','房龄','房间数']
for i in range(3):
    plt.subplot(1,3,i+1)
    plt.hist(x[:,i],bins=20,color='red',edgecolor='black')
    plt.title(titles[i])
    plt.grid(True,alpha=0.5)
plt.tight_layout()
plt.show()

# 图2 各特征 vs 房价散点图
plt.figure(figsize=(15,4))
for i in range(3):
    plt.subplot(1,3,i+1)
    plt.scatter(x[:,i],y,alpha=0.5,color='orange')
    plt.xlabel(titles[i])
    plt.ylabel('房价（万元）')
    plt.grid(True)
plt.tight_layout()
plt.show()

# 图3 实际值 vs 预测值
"""




# 1.生成数据
x,y=make_regression(
    n_samples=300,
    n_features=3,
    noise=10,
    random_state=42
)

# 映射到真实范围
x[:,0]=np.interp(x[:,0],(x[:,0].min(),x[:,0].max()),(0,10))# 学习时间
x[:,1]=np.interp(x[:,1],(x[:,1].min(),x[:,1].max()),(5,9))# 睡眠时间
x[:,2]=np.interp(x[:,2],(x[:,2].min(),x[:,2].max()),(1,5))# 复习次数
x[:,2]=np.round(x[:,2]).astype(int)

y=np.interp(y,(y.min(),y.max()),(0,100))# 成绩
y=np.round(y,2)

print("x shape:",x.shape)
print("y shape:",y.shape)
print("\n 前五行",x[:5])
print("\n 前五个成绩",y[:5])

# 2.划分训练集
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

# 3.训练模型
model=LinearRegression()
model.fit(x_train,y_train)
y_pred=model.predict(x_test)

r2=r2_score(y_test,y_pred)
mae=mean_absolute_error(y_test,y_pred)

print(f"\n模型评估:")
print(f"R² 得分: {r2:.4f}")
print(f"MAE: {mae:.2f} 分")
print(f"回归方程: 成绩 = {model.coef_[0]:.2f}×学习时间 + {model.coef_[1]:.2f}×睡眠时长 + {model.coef_[2]:.2f}×复习次数 + {model.intercept_:.2f}")

fig,axes=plt.subplots(1,3,figsize=(15,4))
axes[0].scatter(x[:,0],y,alpha=0.5,color='orange')
axes[0].set_xlabel('学习时间(小时)')
axes[0].set_ylabel('成绩')
axes[0].set_title('学习时间 vs 成绩')
axes[0].grid(True)


axes[1].scatter(x[:,1],y,alpha=0.5,color='green')
axes[1].set_xlabel('睡眠时间(小时)')
axes[1].set_ylabel('成绩')
axes[1].set_title('睡眠时间 vs 成绩')
axes[1].grid(True)


axes[2].scatter(x[:,2],y,alpha=0.5,color='black')
axes[2].set_xlabel('复习次数')
axes[2].set_ylabel('成绩')
axes[2].set_title('复习次数 vs 成绩')
axes[2].grid(True)

plt.tight_layout()
plt.show()

