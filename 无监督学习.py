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

print("二、无监督学习：客户价值分群聚类模型")

X, _ = datasets.make_blobs(
    n_samples=200,
    n_features=3,
    centers=4,
    random_state=42
)

X[:, 0] = np.interp(X[:, 0], (X[:, 0].min(), X[:, 0].max()), (100, 10000))
X[:, 1] = np.interp(X[:, 1], (X[:, 1].min(), X[:, 1].max()), (3, 15))
X[:, 2] = np.interp(X[:, 2], (X[:, 2].min(), X[:, 2].max()), (20, 500))

print(f"数据形状: X={X.shape}")
print(f"月消费金额范围: {X[:, 0].min():.0f} ~ {X[:, 0].max():.0f} 元")
print(f"月购买频率范围: {X[:, 1].min():.1f} ~ {X[:, 1].max():.1f} 次/月")
print(f"平均订单金额范围: {X[:, 2].min():.0f} ~ {X[:, 2].max():.0f} 元")

model = KMeans(n_clusters=4, random_state=42)
y_pred = model.fit_predict(X)

centers = model.cluster_centers_
print(f"\n聚类中心:")
for i, center in enumerate(centers):
    print(f"  群组{i + 1}: 消费金额={center[0]:.0f}元, 购买频率={center[1]:.1f}次/月, 平均订单金额={center[2]:.0f}元")

plt.figure(figsize=(10, 6))
scatter = plt.scatter(X[:, 0], X[:, 1], c=y_pred, cmap='viridis', alpha=0.6, label='客户')
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='*', s=200, label='聚类中心')
plt.xlabel('月消费金额 (元)')
plt.ylabel('月购买频率 (次)')
plt.title('无监督学习：客户价值分群聚类模型')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()