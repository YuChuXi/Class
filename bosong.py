import random
import math
from tqdm import trange, tqdm
import matplotlib.pyplot as plt

def generate_poisson_samples(lam, size):
    samples = [0] * size
    for i in trange(size):
        L = math.exp(-lam)
        k = 0
        p = 1.0
        while p > L:
            k += 1
            p *= random.random()
        samples[i] = k-1
    return samples

def generate_normal_samples(mu, sig, size):
    samples = [0] * size
    for i in trange(size):
        u1 = random.random()
        u2 = random.random()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        samples[i] = z0 * sig + mu
    return samples

def histogram(data, bins):
    counts = [0] * (len(bins)-1)
    for d in tqdm(data):
        for i in range(len(bins)-1):
            if bins[i] <= d < bins[i+1]:
                counts[i] += 1
                break
    total = sum(counts)
    return [c/total for c in counts]

lam = 5.0
mu = 5.0
sig = 2.0
sample_size = 100000
# 随机采样几万个
poisson_samples = generate_poisson_samples(lam, sample_size)
normal_samples = generate_normal_samples(mu, sig, sample_size)

# 统计概率
poisson_x = list(range(15))
poisson_hist = histogram(poisson_samples, [x-0.5 for x in range(16)])

nn = 100
nw_size = 0.1
norm_x = [x*15/nn for x in range(nn)]
normal_pdf = [sum(1 for n in normal_samples if x-nw_size <= n < x+nw_size)/sample_size/nw_size/2
             for x in tqdm(norm_x)] 

plt.bar(poisson_x, poisson_hist)
plt.plot(norm_x, normal_pdf, 'r-')
plt.show()
