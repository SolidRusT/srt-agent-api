# GPU Tweaks

## AMD ROCm 6.x users

Grab a torch wheel that closely matches your ROCm version and python version.

- [PyTorch Wheels](https://download.pytorch.org/whl/torch/)

For example, with ROCm version 6.1 and Python 3.12:

```bash
pip install wheel setuptools packaging
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.0
# Optional (takes awhile to build)
pip install -U git+https://github.com/ROCm/flash-attention@flash_attention_for_rocm
```

Check if your AMD ROCm CUDA is available in PyTorch:

```bash
python -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'
python -c 'import torch; print(torch.cuda.is_available())'
```
