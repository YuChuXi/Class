import numpy as np
import matplotlib.pyplot as plt

n_points = int(1e5)
points = np.random.rand(n_points, 2) * 2 - 1

distances = np.sqrt(points[:, 0] ** 2 + points[:, 1] ** 2)

inside = distances <= 1.0
outside = ~inside
n_inside = np.sum(inside)
pi_estimate = 4 * n_inside / n_points

plt.figure(figsize=(8, 8))
plt.scatter(points[inside, 0], points[inside, 1], color="red", s=1)
plt.scatter(points[outside, 0], points[outside, 1], color="blue", s=1)

circle = plt.Circle((0, 0), 1, color="green", fill=False, linewidth=1)
plt.gca().add_patch(circle)

plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.title(f"pi: {n_inside}/{n_points}={pi_estimate}")
plt.show()
