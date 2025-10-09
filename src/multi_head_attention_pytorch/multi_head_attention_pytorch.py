import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    def __init__(self, model_d, num_head, dropout, bias=True):
        self.model_d = model_d
        self.num_head = num_head
        self.dropout = nn.Dropout(dropout)
        self.wq = nn.Linear(model_d, model_d, bias=bias)
        self.wk = nn.Linear(model_d, model_d, bias=bias)
        self.wv = nn.Linear(model_d, model_d, bias=bias)
        self.wo = nn.Linear(model_d, model_d, bias=bias)
    
    def forward(self, x, mask):
        B, L = x.shape()
        head_d = model_d // self.num_head
        def getProjection(t, w):
            y = w(t).view(B, L, self.num_head, head_d).transpose(1, 2)
            return y
        q = getProjection(x, self.wq)
        k = getProjection(x, self.wk)
        v = getProjection(x, self.wv)
        score = torch.matmul(q, k.transpose(2, 3)) / (head_d ** 0.5)
        attn = torch.softmax(score)
        attn = self.dropout(attn) + mask
        out = torch.matmul(attn, v)
        out = out.transpose(1, 2).view(B, L, -1)
        out = self.wo(out)
        return out