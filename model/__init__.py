import torch, numpy as np, random, os

np.random.seed(0)
torch.manual_seed(0)
random.seed(0)




# set device
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("| using device:", device)
os.environ["device"] = device
