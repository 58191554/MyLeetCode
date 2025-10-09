# test_mha.py
# 需要你把实现放在 mha.py 中：
# from mha import MultiHeadAttention, make_causal_mask, make_padding_mask

import math
import torch
import pytest

from multi_head_attention_pytorch import MultiHeadAttention as ImplMultiHeadAttention
from multi_head_attention_pytorch_ref import (
    MultiHeadAttention as RefMultiHeadAttention,
    make_causal_mask,
)


def test_output_shapes_self_attention():
    torch.manual_seed(0)
    B, L, d_model, H = 2, 7, 32, 4
    x = torch.randn(B, L, d_model)

    impl = ImplMultiHeadAttention(d_model, H, dropout=0.0)
    ref = RefMultiHeadAttention(d_model, H, dropout=0.0)
    impl.eval(); ref.eval()

    out_i, attn_i = impl(x, None)
    out_r, attn_r = ref(x, None)

    assert out_i.shape == (B, L, d_model)
    assert attn_i.shape == (B, H, L, L)
    assert out_r.shape == (B, L, d_model)
    assert attn_r.shape == (B, H, L, L)


def test_causal_mask_enforces_lower_triangle():
    torch.manual_seed(0)
    B, L, d_model, H = 2, 5, 32, 4
    x = torch.randn(B, L, d_model)

    causal = make_causal_mask(L, L)  # [1,1,L,L]
    impl = ImplMultiHeadAttention(d_model, H, dropout=0.0)
    impl.eval()

    _, attn = impl(x, causal)  # [B,H,L,L]
    # 上三角（j > i）必须为 0
    upper = torch.triu(torch.ones(L, L, dtype=torch.bool), diagonal=1)
    upper = upper.unsqueeze(0).unsqueeze(0).expand(B, H, L, L)
    assert torch.all(attn[upper] == 0.0)


def test_gradients_flow():
    torch.manual_seed(0)
    B, L, d_model, H = 2, 6, 32, 4
    x = torch.randn(B, L, d_model, requires_grad=True)

    mha = ImplMultiHeadAttention(d_model, H, dropout=0.1)  # 测试带dropout也能回传
    out, _ = mha(x, None)
    loss = out.pow(2).mean()
    loss.backward()

    # 参数都有梯度，并且不是 NaN
    for name, p in mha.named_parameters():
        assert p.grad is not None, f"{name} has no grad"
        assert torch.isfinite(p.grad).all(), f"{name} grad has non-finite values"

    # 输入也应有梯度
    assert x.grad is not None
    assert torch.isfinite(x.grad).all()


def test_single_head_equivalence_with_reference():
    torch.manual_seed(42)
    B, L, d_model, H = 2, 6, 16, 1  # 单头
    x = torch.randn(B, L, d_model)

    impl = ImplMultiHeadAttention(d_model, H, dropout=0.0)
    ref = RefMultiHeadAttention(d_model, H, dropout=0.0)
    impl.eval(); ref.eval()

    out_i, attn_i = impl(x, None)
    out_r, attn_r = ref(x, None)

    assert torch.allclose(out_i, out_r, atol=1e-6)
    assert torch.allclose(attn_i, attn_r, atol=1e-6)


def test_mask_broadcasting_equivalence():
    torch.manual_seed(0)
    B, Lq, Lk, d_model, H = 2, 5, 6, 32, 4
    x = torch.randn(B, Lk, d_model)

    # 基础 mask：屏蔽最后一列 key
    base = torch.ones(B, 1, Lq, Lk)
    base[:, :, :, -1] = 0
    expanded = base.expand(B, H, Lq, Lk).clone()

    mha = ImplMultiHeadAttention(d_model, H, dropout=0.0)
    mha.eval()

    out1, attn1 = mha(x, base)
    out2, attn2 = mha(x, expanded)

    assert torch.allclose(out1, out2, atol=1e-6)
    assert torch.allclose(attn1, attn2, atol=1e-6)


def test_numerical_stability_large_scores_no_nan():
    torch.manual_seed(0)
    B, L, d_model, H = 2, 8, 64, 8
    scale = 1000.0  # 制造大的点积
    x = torch.randn(B, L, d_model) * scale

    mha = ImplMultiHeadAttention(d_model, H, dropout=0.0)
    mha.eval()

    out, attn = mha(x, None)
    assert torch.isfinite(out).all()
    assert torch.isfinite(attn).all()
    # 每行注意力仍应在有效范围（和为1）
    sums = attn.sum(dim=-1)
    assert torch.allclose(sums, torch.ones_like(sums), atol=1e-5)


@pytest.mark.parametrize("d_model,H", [(32, 4), (48, 6), (64, 8)])
def test_d_model_divisible_by_heads(d_model, H):
    # 构造一个合法的实例不会抛错
    _ = ImplMultiHeadAttention(d_model, H)

    # 构造一个不合法的实例应当抛 AssertionError
    with pytest.raises(AssertionError):
        _ = ImplMultiHeadAttention(d_model + 1, H)
