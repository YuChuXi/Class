import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize

# 定义函数和梯度
def z(x, y):
    return np.sqrt(np.sin(x)**2 + np.sin(y)**2)

def gradient(x, y):
    dz_dx = (np.sin(x) * np.cos(x)) / (np.sqrt(np.sin(x)**2 + np.sin(y)**2) + 1e-8)
    dz_dy = (np.sin(y) * np.cos(y)) / (np.sqrt(np.sin(x)**2 + np.sin(y)**2) + 1e-8)
    return dz_dx, dz_dy

# 生成网格
x = np.linspace(-np.pi, np.pi, 100)
y = np.linspace(-np.pi, np.pi, 100)
X, Y = np.meshgrid(x, y)
Z = z(X, Y)

# # 随机生成 100 个初始点
# np.random.seed(42)
# initial_points = np.random.uniform(-np.pi, np.pi, (100, 2))

grid = np.mgrid[-np.pi:np.pi:10j, -np.pi:np.pi:10j] * 0.999
initial_points = grid.reshape(2, -1).T


# 梯度下降参数
alpha = 0.1  # 学习率
steps = 100   # 迭代次数
trajectories = []

# 对每个点进行梯度下降并记录完整轨迹
for point in initial_points:
    x_current, y_current = point[0], point[1]
    path = []
    for _ in range(steps):
        path.append([x_current, y_current])
        dz_dx, dz_dy = gradient(x_current, y_current)
        x_current += alpha * dz_dx
        y_current += alpha * dz_dy
    trajectories.append(np.array(path))

# 转换为 NumPy 数组以便索引
trajectories = np.array(trajectories)  # shape: (100, steps, 2)

# 创建画布和颜色映射
fig, ax = plt.subplots(figsize=(10, 8))
norm = Normalize(vmin=0, vmax=steps)
ax.set_xlim(-np.pi, np.pi)
ax.set_ylim(-np.pi, np.pi)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Gradient Descent with Trajectories (100 Points)')

# 绘制背景的等高线
contour = ax.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.5)
plt.colorbar(contour, label='z = sqrt(sin²(x) + sin²(y))')

# 初始化空的散点图和轨迹线
scatter = ax.scatter([], [], c=[], cmap='viridis', s=20, alpha=0.7)
lines = [ax.plot([], [], 'r-', linewidth=0.5, alpha=0.3)[0] for _ in range(100)]

# 动画更新函数
def update(frame):
    # 更新散点图的位置和颜色
    current_positions = trajectories[:, frame, :]
    scatter.set_offsets(current_positions)
    scatter.set_array(np.full(100, frame))
    
    # 更新所有轨迹线（保留历史路径）
    for i in range(100):
        lines[i].set_data(trajectories[i, :frame+1, 0], trajectories[i, :frame+1, 1])
    
    return [scatter] + lines

# 创建动画
ani = FuncAnimation(
    fig, 
    update, 
    frames=steps, 
    interval=100,  # 每帧间隔 100ms
    blit=True
)

# 保存动画为 GIF
ani.save('gradient_descent_with_trajectories.gif', writer='pillow', fps=10)

plt.show()