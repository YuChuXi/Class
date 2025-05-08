import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import matplotlib as mpl

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'Microsoft YaHei']  # 优先使用文泉驿
plt.rcParams['axes.unicode_minus'] = False
# 设置样式
sns.set_style("whitegrid")
sns.set_palette("husl")

# 生成不同分布的随机数
np.random.seed(42)  # 保证可重复性

# 1. 均匀分布
uniform_data = np.random.uniform(0, 100, 1000)
uniform_sorted = np.sort(uniform_data)

# 2. 正态分布
normal_data = np.random.normal(50, 15, 1000)
normal_sorted = np.sort(normal_data)

# 3. 指数分布
exponential_data = np.random.exponential(20, 1000)
exponential_sorted = np.sort(exponential_data)

# 4. 泊松分布
poisson_data = np.random.poisson(10, 1000)
poisson_sorted = np.sort(poisson_data)

# 5. 对数正态分布
lognormal_data = np.random.lognormal(3, 0.5, 1000)
lognormal_sorted = np.sort(lognormal_data)

# 创建图形
plt.figure(figsize=(15, 10), dpi=100)

# 绘制排序后的数据
plt.subplot(2, 3, 1)
plt.plot(uniform_sorted)
plt.title('均匀分布 (排序后)')
plt.xlabel('索引')
plt.ylabel('数值')

plt.subplot(2, 3, 2)
plt.plot(normal_sorted)
plt.title('正态分布 (排序后)')
plt.xlabel('索引')
plt.ylabel('数值')

plt.subplot(2, 3, 3)
plt.plot(exponential_sorted)
plt.title('指数分布 (排序后)')
plt.xlabel('索引')
plt.ylabel('数值')

plt.subplot(2, 3, 4)
plt.plot(poisson_sorted)
plt.title('泊松分布 (排序后)')
plt.xlabel('索引')
plt.ylabel('数值')

plt.subplot(2, 3, 5)
plt.plot(lognormal_sorted)
plt.title('对数正态分布 (排序后)')
plt.xlabel('索引')
plt.ylabel('数值')

# 添加分布直方图对比
plt.subplot(2, 3, 6)
sns.histplot(uniform_data, color='blue', label='均匀分布', kde=True, alpha=0.3)
sns.histplot(normal_data, color='green', label='正态分布', kde=True, alpha=0.3)
sns.histplot(exponential_data, color='red', label='指数分布', kde=True, alpha=0.3)
sns.histplot(poisson_data, color='purple', label='泊松分布', kde=True, alpha=0.3)
sns.histplot(lognormal_data, color='orange', label='对数正态分布', kde=True, alpha=0.3)
plt.title('不同概率分布对比')
plt.xlabel('数值')
plt.ylabel('频率')
plt.legend()

plt.tight_layout()

# 保存图表到文件
plt.savefig('不同分布对比图.png', dpi=300, bbox_inches='tight')
print("图表已保存为 不同分布对比图.png")

plt.show()