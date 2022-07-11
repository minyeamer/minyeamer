import torch

# torch.__version__
# 1.13.0.dev20220710

# device setting, nvidia='cuda:0' | m1='mps' | cpu='cpu'
device = torch.device('mps')
print(f' - device : {device}')

sample = torch.Tensor([[10, 20, 30], [30, 20, 10]])
print(f' - cpu tensor : ')
print(sample)

sample = sample.to(device)
print(f' - gpu tensor : ')
print(sample)
