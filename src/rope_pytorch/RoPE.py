"""
cos_all =
row0: [ 0,  0]
row1: [ 1, -1]
row2: [ 2, -2]
row3: [ 3, -3]
row4: [ 4, -4]
row5: [ 5, -5]
row6: [ 6, -6]
row7: [ 7, -7]
row8: [ 8, -8]
row9: [ 9, -9]

pos = [[3,4,5],
       [5,6,7]]

index_select 后的矩阵 =
[
  cos_all[3] = [3, -3],
  cos_all[4] = [4, -4],
  cos_all[5] = [5, -5],
  cos_all[5] = [5, -5],
  cos_all[6] = [6, -6],
  cos_all[7] = [7, -7],
]
"""

from typing import List
import torch
import torch.nn as nn

class RoPE(nn.Module):
    def __init__(self, dim: int, seq_len: int, base: float = 10000.0):
        super().__init__()
        assert dim % 2 == 0
        self.dim = dim
        self.seq_len = seq_len
        self.half_dims = dim // 2
        half_dims = dim // 2
        inner = torch.arange(0, half_dims, dtype=torch.float32) / float(half_dims)
        freqs = torch.pow(torch.tensor(base, dtype=torch.float32), -inner)
        t = torch.arange(seq_len, dtype=torch.float32)
        freqs = torch.outer(t, freqs)
        self.register_buffer("cos_freqs_f32", torch.cos(freqs), persistent=False)
        self.register_buffer("sin_freqs_f32", torch.sin(freqs), persistent=False)
    
    def _make_bias(self, S: int, N: int, device: torch.device, dtype: torch.dtype, offset: List[slice]) -> (torch.Tensor, torch.Tensor):
        cos_all = self.cos_freqs_f32.to(device=device, dtype=dtype)
        sin_all = self.sin_freqs_f32.to(device=device, dtype=dtype)
        
        pos = []
        for o in offset:
            pos.append(torch.arange(o.start, o.stop, device=device, dtype=torch.long))
        pos = torch.stack(pos, dim=0)
        
        cos = cos_all.index_select(0, pos.view(-1)).view(N, S, self.half_dims)
        sin = sin_all.index_select(0, pos.view(-1)).view(N, S, self.half_dims)
        # 扩到 [N, S, 1, half]，head 维用广播
        cos = cos.unsqueeze(2)
        sin = sin.unsqueeze(2)
        return cos, sin
    
    def forward(self, x: torch.Tensor, offset: List[slice]) -> torch.Tensor:
        N, S, H, D = x.shape
        device, dtype = x.device, x.dtype
        
        cos_bias, sin_bias = self._make_bias(S, N, device=device, dtype=dtype, offset=offset)
        x = x.view(N, S, H, D // 2, 2)
        x1 = x[..., 0]
        x2 = x[..., 1]
        real = x1 * cos_bias - x2 * sin_bias
        imag = x2 * cos_bias + x1 * sin_bias
        y = torch.stack([real, imag], dim=-1)
        y = y.reshape(N, S, H, D)
        return y.to(dtype=dtype)
    
    
