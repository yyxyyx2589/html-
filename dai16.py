import pandas as pd
from pandas import DataFrame as df
"""student_data={
    '姓名':['小明','小红'],
    '科目':['数学','语文'],
    '成绩':[99,98]
}
student_grades=pd.DataFrame(student_data)
print(student_grades)"""


data=pd.read_csv(r"C:\Users\yyx\Desktop\shi_xun\package\student_scores.csv")
#print(data)

"""print(data)
print(df.head(data))
print(df.tail(data))
print(data.shape)
print(data.info())
print(data.describe())"""

"""#行列
print(data['科目'])
print(data[['科目','成绩']])
print(data.loc[[0,1]])
print(data.iloc[[4]])
print(data.loc[0:2,['科目']])

#筛选
print(data[data['成绩']>80])"""

print(data.isnull().sum())#统计缺失值的数量
#data=data.dropna()#删除缺失值的行
#print(data)
"""data.fillna({'成绩':data['成绩'].mean()},inplace=True)#均值填充缺失值
print(data)

print("\n查看重复行")
print(data[data.duplicated(subset=['姓名','科目'],keep=False)])

print("\n删除重复行")
print(data.drop_duplicates(subset=['姓名','科目'],keep='first'))

print("\n按科目分组，求平均分")
avg=data.groupby("科目")["成绩"].mean()
print(avg)

print("\n按班级和性别分组，求最高成就")
max_grade=data.groupby(['班级','性别'])['成绩'].max()
print(max_grade)

print("\n新增总分")
data['总成绩']=data['成绩']+data['平时分']
print(data)

print("\n修改成绩")
data['修改后的成绩']=data['成绩'].apply(lambda x:min(x+5,100))
print(data)

print("\n按成绩降序排序")
score=data.sort_values(by='成绩',ascending=False)
print(score)"""


