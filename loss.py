import torch
import math

x1 = torch.rand((1000)) * 10
x2 = torch.rand((1000)) * 10 + 5
x3 = torch.rand((1000)) * 15 + 5

y = x1 * 3 + x2 * 5 + x3 * 7

e = 50000
ilr = 0.001
flr = 0.0

(a, b, c) = (-1, -1, -1)
for i in range(e):
    pred_y = x1 * a + x2 * b + x3 * c
    loss = ((pred_y - y) ** 2).mean()
    lr = (math.cos((i) * (math.pi / (e))) * 0.5 + 0.5) * (ilr - flr) + flr

    ly = pred_y - y
    ga = 2 * ((x1 * ly).mean())
    gb = 2 * ((x2 * ly).mean())
    gc = 2 * ((x3 * ly).mean())

    a -= ga * lr
    b -= gb * lr
    c -= gc * lr

    print("i: ", i, "loss: ", loss.item(), "lr: ", lr)

print((a, b, c))
print(5 * a + 10 * b + 9 * c)
