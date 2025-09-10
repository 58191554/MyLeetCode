import numpy as np

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def loss_and_grads(W, b, X, y, l2=0.0, eps=1e-12):
    N = X.shape[0]
    z = X @ W + b
    p = sigmoid(z)
    
    p_clip = np.clip(p, eps, 1 - eps)
    loss = -np.mean(y * np.log(p_clip) + (1 - y) * np.log(1 - p_clip))
    
    diff = (p - y) / N
    dW = X.T @ diff + l2 * W
    db = np.sum(diff)
    
    return loss, dW, db

def gd_step(W, b, dW, db, lr):
    W -= lr * dW
    b -= lr * db
    return W, b

def make_synthetic(n=256, d=10, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d))
    true_W = rng.normal(size=(d,))
    true_b = 0.3
    logits = X @ true_W + true_b
    p = sigmoid(logits)
    y = (rng.uniform(size=n) < p).astype(np.float64)
    return X, y

def train_demo():
    X, y = make_synthetic(n=512, d=20, seed=42)
    N, D = X.shape
    W = np.zeros(D)
    b = 0.0
    l2 = 1e-2
    lr = 1.0   

    for t in range(200):
        loss, dW, db = loss_and_grads(W, b, X, y, l2=l2)
        W, b = gd_step(W, b, dW, db, lr)
        if (t+1) % 20 == 0:
            # 简单评估
            p = sigmoid(X @ W + b)
            pred = (p >= 0.5).astype(np.float64)
            acc = (pred == y).mean()
            print(f"step {t+1:3d} | loss={loss:.4f} | acc={acc:.3f}")

    return W, b

if __name__ == "__main__":
    train_demo()