import torch
import torch.nn as nn
import torch.nn.functional as F

N = 512
D = 16
X = torch.randn(N, D)
W_real = torch.randn(D)
b_real = torch.randn(1)
logits = X @ W_real + b_real
p = torch.sigmoid(logits)
y_real = torch.bernoulli(p).to(dtype=torch.float32)

model = nn.Linear(D, 1)
nn.init.zeros_(model.weight)
nn.init.zeros_(model.bias)

weight_decay = 1e-2
lr = 1.0
optimizer = torch.optim.SGD(model.parameters(), lr=lr, weight_decay=weight_decay)

steps = 1000
for t in range(steps):
    optimizer.zero_grad()
    logits = model(X).squeeze(1)
    p = torch.sigmoid(logits)
    p = p.clamp(1e-12, 1 - 1e-12)
    loss = -(y_real * torch.log(p) + (1 - y_real) * torch.log(1 - p)).mean()
    loss.backward()
    optimizer.step()
    if (t + 1) % 20 == 0:
        with torch.no_grad():
            prob = torch.sigmoid(logits)
            pred = (prob >= 0.5).to(dtype=y_real.dtype)
            acc = (pred == y_real).to(dtype=torch.float32).mean().item()
        print(f"step {t+1:3d} | loss={loss.item():.4f} | acc={acc:.3f}")

print(model.weight)
print(model.bias)
