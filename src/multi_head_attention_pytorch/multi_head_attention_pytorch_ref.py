import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    """
        input: q, k, v: [B x L x dim]
        
    """
    def __init__(self, d_model: int, num_heads: int, dropout: float=0., bias: bool = True):
        super().__init__()
        assert d_model % num_heads == 0
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_head = d_model // num_heads
        self.W_q = nn.Linear(d_model, d_model, bias=bias)
        self.W_k = nn.Linear(d_model, d_model, bias=bias)
        self.W_v = nn.Linear(d_model, d_model, bias=bias)
        self.W_o = nn.Linear(d_model, d_model, bias=bias)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x: torch.Tensor, mask=None):
        B, Lq, _ = q.shape
        Lk = k.shape[1]
        
        q = self.W_q(q)
        k = self.W_k(k)
        v = self.W_v(v)
        
        q = q.view(B, -1, self.num_heads, self.d_head).transpose(1, 2)
        k = k.view(B, -1, self.num_heads, self.d_head).transpose(1, 2)
        v = v.view(B, -1, self.num_heads, self.d_head).transpose(1, 2)

        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.d_head ** 0.5)
        
        if mask is not None:
            scores = scores.masked_fill(mask==0, float("-inf"))
        
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)
        
        out = torch.matmul(attn, v)
        out = out.transpose(1, 2).contiguous().view(B, Lq, self.d_model)
        out = self.W_o(out)
        return out, attn

def make_causal_mask(Lq: int, Lk: int):
    mask = torch.tril(torch.ones(Lq, Lk))
    return mask.unsqueeze(0).unsqueeze(0)
    