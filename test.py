import torch

# Check if PyTorch is using GPU (if available)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Create a tensor and move it to the selected device
x = torch.rand(5, 5).to(device)
print(f"Tensor on {device}:")
print(x)
