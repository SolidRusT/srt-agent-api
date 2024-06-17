# GPU Tweaks

## AMD ROCm 6.x users

Grab a torch wheel that closely matches your ROCm version and python version.

- [PyTorch Wheels](https://download.pytorch.org/whl/torch/)

For example, with ROCm version 6.1 and Python 3.12:

```bash
wget https://download.pytorch.org/whl/rocm6.0/torch-2.3.1%2Brocm6.0-cp312-cp312-linux_x86_64.whl#sha256=7d0aac31a5d76a6f737238725baecf35a6924f333f60a075ef5856c9e3212045
pip install torch-2.3.1+rocm6.0-cp312-cp312-linux_x86_64.whl
```
