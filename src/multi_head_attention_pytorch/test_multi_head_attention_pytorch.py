# test_mha.py
# 需要你把实现放在 mha.py 中：
# from mha import MultiHeadAttention, make_causal_mask, make_padding_mask

import math
import torch
import pytest

from multi_head_attention_pytorch import MultiHeadAttention, make_causal_mask


def test_output_shapes_self_attention():
    torch.manual_seed(0)
    B, L, d_model, H = 2, 7, 32, 4
    x = torch.randn(B, L, d_model)

    mha = MultiHeadAttention(d_model, H, dropout=0.0)
    mha.eval()

    out, attn = mha(x, x, x)
    assert out.shape == (B, L, d_model)
    assert attn.shape == (B, H, L, L)


def test_cross_attention_shapes():
    torch.manual_seed(0)
    B, Lq, Lk, d_model, H = 2, 5, 8, 48, 6
    q = torch.randn(B, Lq, d_model)
    k = torch.randn(B, Lk, d_model)
    v = torch.randn(B, Lk, d_model)

    mha = MultiHeadAttention(d_model, H, dropout=0.0)
    mha.eval()

    out, attn = mha(q, k, v)
    assert out.shape == (B, Lq, d_model)
    assert attn.shape == (B, H, Lq, Lk)


def test_causal_mask_enforces_lower_triangle():
    torch.manual_seed(0)
    B, L, d_model, H = 2, 5, 32, 4
    x = torch.randn(B, L, d_model)

    causal = make_causal_mask(L, L)  # [1,1,L,L]
    mha = MultiHeadAttention(d_model, H, dropout=0.0)
    mha.eval()

    out, attn = mha(x, x, x, mask=causal)  # [B,H,L,L]
    # 上三角（j > i）必须为 0
    upper = torch.triu(torch.ones(L, L, dtype=torch.bool), diagonal=1)
    upper = upper.unsqueeze(0).unsqueeze(0).expand(B, H, L, L)
    assert torch.all(attn[upper] == 0.0)


def test_gradients_flow():
    torch.manual_seed(0)
    B, L, d_model, H = 2, 6, 32, 4
    x = torch.randn(B, L, d_model, requires_grad=True)

    mha = MultiHeadAttention(d_model, H, dropout=0.1)  # 测试带dropout也能回传
    out, _ = mha(x, x, x)
    loss = out.pow(2).mean()
    loss.backward()

    # 参数都有梯度，并且不是 NaN
    for name, p in mha.named_parameters():
        assert p.grad is not None, f"{name} has no grad"
        assert torch.isfinite(p.grad).all(), f"{name} grad has non-finite values"

    # 输入也应有梯度
    assert x.grad is not None
    assert torch.isfinite(x.grad).all()


def test_single_head_equivalence_with_manual_attention():
    torch.manual_seed(42)
    B, Lq, Lk, d_model, H = 2, 4, 5, 16, 1  # 单头
    q = torch.randn(B, Lq, d_model)
    k = torch.randn(B, Lk, d_model)
    v = torch.randn(B, Lk, d_model)

    mha = MultiHeadAttention(d_model, H, dropout=0.0)
    mha.eval()

    out1, attn1 = mha(q, k, v)

    # 手动等价实现（单头）
    with torch.no_grad():
        q_lin = mha.W_q(q)  # [B,Lq,d]
        k_lin = mha.W_k(k)  # [B,Lk,d]
        v_lin = mha.W_v(v)  # [B,Lk,d]

        d_head = d_model  # 单头 == d_model
        qh = q_lin.view(B, Lq, 1, d_head).transpose(1, 2)  # [B,1,Lq,d]
        kh = k_lin.view(B, Lk, 1, d_head).transpose(1, 2)  # [B,1,Lk,d]
        vh = v_lin.view(B, Lk, 1, d_head).transpose(1, 2)  # [B,1,Lk,d]

        scores = torch.matmul(qh, kh.transpose(-2, -1)) / math.sqrt(d_head)  # [B,1,Lq,Lk]
        attn = torch.softmax(scores, dim=-1)
        out = torch.matmul(attn, vh)  # [B,1,Lq,d]
        out = out.transpose(1, 2).contiguous().view(B, Lq, d_model)
        out2 = mha.W_o(out)

    assert torch.allclose(out1, out2, atol=1e-6)
    assert torch.allclose(attn1, attn, atol=1e-6)


def test_mask_broadcasting_equivalence():
    torch.manual_seed(0)
    B, Lq, Lk, d_model, H = 2, 5, 6, 32, 4
    q = torch.randn(B, Lq, d_model)
    k = torch.randn(B, Lk, d_model)
    v = torch.randn(B, Lk, d_model)

    # 基础 mask：屏蔽最后一列 key
    base = torch.ones(B, 1, Lq, Lk)
    base[:, :, :, -1] = 0
    expanded = base.expand(B, H, Lq, Lk).clone()

    mha = MultiHeadAttention(d_model, H, dropout=0.0)
    mha.eval()

    out1, attn1 = mha(q, k, v, mask=base)
    out2, attn2 = mha(q, k, v, mask=expanded)

    assert torch.allclose(out1, out2, atol=1e-6)
    assert torch.allclose(attn1, attn2, atol=1e-6)


def test_numerical_stability_large_scores_no_nan():
    torch.manual_seed(0)
    B, L, d_model, H = 2, 8, 64, 8
    scale = 1000.0  # 制造大的点积
    x = torch.randn(B, L, d_model) * scale

    mha = MultiHeadAttention(d_model, H, dropout=0.0)
    mha.eval()

    out, attn = mha(x, x, x)
    assert torch.isfinite(out).all()
    assert torch.isfinite(attn).all()
    # 每行注意力仍应在有效范围（和为1）
    sums = attn.sum(dim=-1)
    assert torch.allclose(sums, torch.ones_like(sums), atol=1e-5)


@pytest.mark.parametrize("d_model,H", [(32, 4), (48, 6), (64, 8)])
def test_d_model_divisible_by_heads(d_model, H):
    # 构造一个合法的实例不会抛错
    _ = MultiHeadAttention(d_model, H)

    # 构造一个不合法的实例应当抛 AssertionError
    with pytest.raises(AssertionError):
        _ = MultiHeadAttention(d_model + 1, H)
