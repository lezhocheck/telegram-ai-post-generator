import torch
from torch.backends.mps import is_available as mps_supported
from torch.cuda import is_available as cuda_supported


def select_device() -> torch.device:
    if mps_supported():
        return torch.device('mps')
    if cuda_supported():
        return torch.device('cuda')
    return torch.device('cpu')