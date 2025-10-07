import torch
import torch.nn as nn
import torch.nn.functional as F

N = 512
D = 16
# compute the X and y_real
X = torch.randn(N, D)
W_real = torch.randn(D, 1)
b_real = torch.randn(1)
logits = X @ W_real + b_real
p = torch.sigmoid(logits)
y_real = torch.bernoulli(p).to(dtype=torch.float32)

# create the model
model = nn.Linear(D, 1)

# train the model
lr = 0.01
optimizer = torch.optim.SGD(model.parameters(), lr=lr)

epoch = 100
for ep in range(epoch):
    optimizer.zero_grad()
    logits = model(X)
    p = torch.sigmoid(logits)
    p = p.clamp(1e-12, 1 - 1e-12)
    loss = -(y_real * torch.log(p) + (1 - y_real) * torch.log(1 - p)).mean()
    loss.backward()
    optimizer.step()
    if (ep + 1) % 20 == 0:
        with torch.no_grad():
            prob = torch.sigmoid(logits)
            pred = (prob > 0.5).to(dtype=torch.float32)
            acc = (pred == y_real).to(dtype=torch.float32).mean().item()
        print("step:{}, loss:{}, acc:{}".format(ep, loss.item(), acc))

print(model.weight)
print(model.bias)