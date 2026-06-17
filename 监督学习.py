import numpy as np
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, mean_absolute_error

print("一、监督学习：学生成绩预测回归模型")

x, y = datasets.make_regression(
    n_samples=100,
    n_features=3,
    noise=8,
    random_state=42
)

x[:, 0] = np.interp(x[:, 0], (x[:, 0].min(), x[:, 0].max()), (0, 10))
x[:, 1] = np.interp(x[:, 1], (x[:, 1].min(), x[:, 1].max()), (5, 9))
x[:, 2] = np.interp(x[:, 2], (x[:, 2].min(), x[:, 2].max()), (1, 5))
x[:, 2] = np.round(x[:, 2]).astype(int)

y = np.interp(y, (y.min(), y.max()), (0, 100))
y = np.round(y, 2)

print(f"数据形状: x={x.shape}, y={y.shape}")
print(f"学习时间范围: {x[:, 0].min():.1f} ~ {x[:, 0].max():.1f} 小时")
print(f"睡眠时长范围: {x[:, 1].min():.1f} ~ {x[:, 1].max():.1f} 小时")
print(f"复习次数范围: {x[:, 2].min():.1f} ~ {x[:, 2].max():.1f} 次")
print(f"考试成绩范围: {y.min():.1f} ~ {y.max():.1f} 分")

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

model = LinearRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f"\n模型评估:")
print(f"R² 得分: {r2:.4f}")
print(f"MAE: {mae:.2f} 分")
print(
    f"回归方程: 成绩 = {model.coef_[0]:.2f}×学习时间 + {model.coef_[1]:.2f}×睡眠时长 + {model.coef_[2]:.2f}×复习次数 + {model.intercept_:.2f}")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
axes[0].scatter(x[:, 0], y, color='skyblue', alpha=0.6)
axes[0].set_xlabel('学习时间(小时)')
axes[0].set_ylabel('考试成绩(分)')
axes[0].set_title('学习时间 vs 成绩')
axes[0].grid(True, linestyle='--', alpha=0.3)

axes[1].scatter(x[:, 1], y, color='green', alpha=0.6)
axes[1].set_xlabel('睡眠时长(小时)')
axes[1].set_ylabel('考试成绩(分)')
axes[1].set_title('睡眠时长 vs 成绩')
axes[1].grid(True, linestyle='--', alpha=0.3)

axes[2].scatter(x[:, 2], y, color='orange', alpha=0.6)
axes[2].set_xlabel('复习次数(次)')
axes[2].set_ylabel('考试成绩(分)')
axes[2].set_title('复习次数 vs 成绩')
axes[2].grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()