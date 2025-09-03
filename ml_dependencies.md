# ML Prerequisites

- Python 3.9+
- macOS (tested) or Linux
- conda or miniconda

## Environment Setup

### 1. Create Conda Environment

```bash
conda create --name llm-training python=3.9 -y
conda activate llm-training
```

### 2. Install PyTorch

Follow the official [PyTorch installation guide](https://pytorch.org/get-started/locally/) for your system.

For macOS (Apple Silicon):
```bash
pip install torch torchvision torchaudio
```

For Linux with CUDA 11.8:
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

For Linux with CUDA 12.1:
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

### 3. Install DeepSpeed

```bash
# Install required dependency first
pip install py-cpuinfo

# Install DeepSpeed
pip install deepspeed
```

### 4. Additional Dependencies (Optional)

For enhanced functionality, you may want to install:

```bash
# For Flash Attention (if available for your platform)
pip install flash-attn --no-build-isolation

# For model utilities
pip install transformers datasets tokenizers

# For experiment tracking
pip install wandb tensorboard

# For data processing
pip install numpy pandas

# For configuration management
pip install hydra-core omegaconf
```

## Verification

Verify your installation:

```bash
python -c "
import torch
import deepspeed
print(f'PyTorch: {torch.__version__}')
print(f'DeepSpeed: {deepspeed.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'MPS available: {torch.backends.mps.is_available()}')
"
```

Expected output should show:
- PyTorch version (e.g., 2.8.0)
- DeepSpeed version (e.g., 0.17.5)
- Hardware acceleration status

## Hardware Support

### macOS (Apple Silicon)
- **GPU Acceleration**: Metal Performance Shaders (MPS)
- **DeepSpeed**: CPU-only features available
- **Flash Attention**: Limited support

### Linux with NVIDIA GPU
- **GPU Acceleration**: CUDA
- **DeepSpeed**: Full GPU acceleration support
- **Flash Attention**: Full support with compatible GPUs

## Common Issues and Solutions

### 1. DeepSpeed Installation Fails

If you encounter `ModuleNotFoundError: No module named 'cpuinfo'`:
```bash
pip install py-cpuinfo
pip install deepspeed
```

### 2. Flash Attention Installation Issues

Flash Attention may not be available for all platforms. Skip if installation fails:
```bash
# This is optional and may fail on some systems
pip install flash-attn --no-build-isolation
```

### 3. CUDA Version Mismatch

Ensure your PyTorch CUDA version matches your system CUDA:
```bash
# Check system CUDA version
nvcc --version

# Install matching PyTorch version
conda install pytorch torchvision torchaudio pytorch-cuda=<YOUR_CUDA_VERSION> -c pytorch -c nvidia
```

## Environment Activation

Always activate the environment before running training scripts:

```bash
conda activate llm-training
cd /path/to/train_gpt_rope_flash_deepspeed
python train_gpt_rope_flash_deepspeed.py
```

## DeepSpeed Configuration

DeepSpeed automatically detects your hardware accelerator:
- **macOS**: Uses MPS accelerator
- **Linux with CUDA**: Uses CUDA accelerator
- **CPU-only**: Falls back to CPU

## Next Steps

1. Ensure all dependencies are installed
2. Verify hardware acceleration is working
3. Configure your training parameters
4. Run your training script

For more information on DeepSpeed configuration, visit: https://www.deepspeed.ai/
