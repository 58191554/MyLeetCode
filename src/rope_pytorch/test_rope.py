import pytest
import torch
import torch.nn as nn
from RoPE import RoPE


class TestRoPE:
    """Test suite for RoPE (Rotary Position Embedding) implementation."""

    def test_rope_initialization_basic(self):
        """Test basic RoPE initialization with valid parameters."""
        dim = 64
        seq_len = 128
        rope = RoPE(dim=dim, seq_len=seq_len)
        
        assert rope.dim == dim
        assert rope.seq_len == seq_len
        assert hasattr(rope, 'cos_freqs_f32')
        assert hasattr(rope, 'sin_freqs_f32')
        assert rope.cos_freqs_f32.shape == (seq_len, dim // 2)
        assert rope.sin_freqs_f32.shape == (seq_len, dim // 2)

    def test_rope_initialization_with_custom_base(self):
        """Test RoPE initialization with custom base parameter."""
        dim = 32
        seq_len = 64
        base = 5000.0
        rope = RoPE(dim=dim, seq_len=seq_len, base=base)
        
        assert rope.dim == dim
        assert rope.seq_len == seq_len

    def test_rope_initialization_invalid_dim(self):
        """Test that RoPE raises assertion error for odd dimensions."""
        with pytest.raises(AssertionError):
            RoPE(dim=33, seq_len=128)  # Odd dimension should fail

    @pytest.mark.parametrize("dim,seq_len", [
        (64, 128),
        (128, 256),
        (32, 64),
        (512, 1024)
    ])
    def test_rope_initialization_various_sizes(self, dim, seq_len):
        """Test RoPE initialization with various dimension and sequence length combinations."""
        rope = RoPE(dim=dim, seq_len=seq_len)
        assert rope.dim == dim
        assert rope.seq_len == seq_len
        assert rope.cos_freqs_f32.shape == (seq_len, dim // 2)
        assert rope.sin_freqs_f32.shape == (seq_len, dim // 2)

    def test_forward_pass_basic(self):
        """Test basic forward pass with simple input."""
        dim = 64
        seq_len = 128
        batch_size = 2
        num_heads = 8
        
        rope = RoPE(dim=dim, seq_len=seq_len)
        
        # Create input tensor [N, S, H, D]
        x = torch.randn(batch_size, seq_len, num_heads, dim)
        offset = [slice(0, seq_len) for _ in range(batch_size)]
        
        output = rope(x, offset)
        
        assert output.shape == x.shape
        assert output.dtype == x.dtype
        assert output.device == x.device

    def test_forward_pass_with_different_offsets(self):
        """Test forward pass with different offset patterns."""
        dim = 32
        seq_len = 64
        batch_size = 3
        num_heads = 4
        
        rope = RoPE(dim=dim, seq_len=seq_len)
        x = torch.randn(batch_size, 32, num_heads, dim)  # Shorter sequence than max
        
        # Different offset patterns
        offset = [
            slice(0, 32),    # Start from beginning
            slice(10, 42),   # Middle section
            slice(32, 64)    # End section
        ]
        
        output = rope(x, offset)
        assert output.shape == x.shape

    def test_forward_pass_different_dtypes(self):
        """Test forward pass with different data types."""
        dim = 32
        seq_len = 64
        rope = RoPE(dim=dim, seq_len=seq_len)
        
        for dtype in [torch.float32, torch.float16, torch.bfloat16]:
            if dtype == torch.bfloat16 and not torch.cuda.is_available():
                continue  # Skip bfloat16 on CPU
                
            x = torch.randn(2, 32, 4, dim, dtype=dtype)
            offset = [slice(0, 32), slice(0, 32)]
            
            output = rope(x, offset)
            assert output.dtype == dtype
            assert output.shape == x.shape

    @pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
    def test_forward_pass_cuda(self):
        """Test forward pass on CUDA device."""
        dim = 64
        seq_len = 128
        rope = RoPE(dim=dim, seq_len=seq_len)
        
        x = torch.randn(2, 64, 8, dim, device='cuda')
        offset = [slice(0, 64), slice(0, 64)]
        
        output = rope(x, offset)
        assert output.device.type == 'cuda'
        assert output.shape == x.shape

    def test_make_bias_function(self):
        """Test the internal _make_bias function."""
        dim = 32
        seq_len = 64
        rope = RoPE(dim=dim, seq_len=seq_len)
        
        S = 32
        N = 2
        device = torch.device('cpu')
        dtype = torch.float32
        offset = [slice(0, 32), slice(16, 48)]
        
        cos_bias, sin_bias = rope._make_bias(S, N, device, dtype, offset)
        
        assert cos_bias.shape == (N, S, 1, dim // 2)
        assert sin_bias.shape == (N, S, 1, dim // 2)
        assert cos_bias.device == device
        assert sin_bias.device == device
        assert cos_bias.dtype == dtype
        assert sin_bias.dtype == dtype

    def test_rotary_property(self):
        """Test that RoPE maintains the rotary property."""
        dim = 32
        seq_len = 64
        rope = RoPE(dim=dim, seq_len=seq_len)
        
        # Create a simple test vector
        x = torch.zeros(1, 2, 1, dim)
        x[0, 0, 0, 0] = 1.0  # Set first element to 1
        x[0, 1, 0, 2] = 1.0  # Set third element to 1 (different pair)
        
        offset = [slice(0, 2)]
        output = rope(x, offset)
        
        # Check that the transformation preserves magnitude for each pair
        # Each pair (x1, x2) should have ||(x1', x2')||_2 == ||(x1, x2)||_2
        input_pairs = x.view(1, 2, 1, dim // 2, 2)
        output_pairs = output.view(1, 2, 1, dim // 2, 2)
        
        input_norms = torch.norm(input_pairs, dim=-1)
        output_norms = torch.norm(output_pairs, dim=-1)
        
        torch.testing.assert_close(input_norms, output_norms, atol=1e-6, rtol=1e-6)

    def test_position_dependence(self):
        """Test that RoPE produces different outputs for different positions."""
        dim = 32
        seq_len = 64
        rope = RoPE(dim=dim, seq_len=seq_len)
        
        # Same input at different positions
        x = torch.ones(1, 2, 1, dim)
        
        # Different offsets
        offset1 = [slice(0, 2)]
        offset2 = [slice(10, 12)]
        
        output1 = rope(x, offset1)
        output2 = rope(x, offset2)
        
        # Outputs should be different due to different positions
        assert not torch.allclose(output1, output2, atol=1e-6)

    def test_gradient_flow(self):
        """Test that gradients flow properly through RoPE."""
        dim = 32
        seq_len = 64
        rope = RoPE(dim=dim, seq_len=seq_len)
        
        x = torch.randn(2, 32, 4, dim, requires_grad=True)
        offset = [slice(0, 32), slice(0, 32)]
        
        output = rope(x, offset)
        loss = output.sum()
        loss.backward()
        
        assert x.grad is not None
        assert x.grad.shape == x.shape

    def test_batch_consistency(self):
        """Test that batched computation gives same results as individual computations."""
        dim = 32
        seq_len = 64
        rope = RoPE(dim=dim, seq_len=seq_len)
        
        # Create batched input
        x_batch = torch.randn(2, 32, 4, dim)
        offset_batch = [slice(0, 32), slice(0, 32)]
        
        # Compute batched result
        output_batch = rope(x_batch, offset_batch)
        
        # Compute individual results
        x1 = x_batch[0:1]
        x2 = x_batch[1:2]
        offset1 = [slice(0, 32)]
        offset2 = [slice(0, 32)]
        
        output1 = rope(x1, offset1)
        output2 = rope(x2, offset2)
        
        # Combine individual results
        output_individual = torch.cat([output1, output2], dim=0)
        
        torch.testing.assert_close(output_batch, output_individual, atol=1e-6, rtol=1e-6)

    @pytest.mark.parametrize("seq_len_used", [16, 32, 64])
    def test_various_sequence_lengths(self, seq_len_used):
        """Test RoPE with various sequence lengths within the maximum."""
        dim = 32
        seq_len_max = 128
        rope = RoPE(dim=dim, seq_len=seq_len_max)
        
        x = torch.randn(1, seq_len_used, 4, dim)
        offset = [slice(0, seq_len_used)]
        
        output = rope(x, offset)
        assert output.shape == x.shape


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
