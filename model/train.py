import torch, random, numpy as np
import copy
from .base import MLP
# set random seeds
np.random.seed(0)
torch.manual_seed(0)
random.seed(0)

# set device
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("| using device:", device)

criterion = torch.nn.CrossEntropyLoss()


def train_client(training_data, global_model, num_local_epochs, lr, optim : torch.optim.Optimizer = torch.optim.SGD) -> MLP:
    local_model = copy.deepcopy(global_model)
    local_model = local_model.to(device)
    local_model.train()

    optimizer = optim(local_model.parameters(), lr=lr)

    for epoch in range(num_local_epochs):
        for (i, (x,y)) in enumerate(training_data):
            x = x.to(device)
            y = y.to(device)
            optimizer.zero_grad()
            out = local_model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
        # print(str(epoch) + ": \n" + str(local_model.state_dict()))
        print("epoch: " + str(epoch))
    return local_model

# def train_client(training_data, global_model, num_local_epochs, lr,  optim : torch.optim.Optimizer = torch.optim.SGD) ->MLP:

#     epsilon = 1
#     local_model = copy.deepcopy(global_model)
#     local_model = local_model.to(device)
#     local_model.train()

#     for epoch in range(num_local_epochs):
#         for i, (x, y) in enumerate(training_data):
#             x = x.to(device)
#             y = y.to(device)

#             # Zero the gradients
#             local_model.zero_grad()

#             # Forward pass
#             output = local_model(x)

#             # Compute the loss
#             loss = criterion(output, y)

#             # Backward pass
#             loss.backward()

#             # Add noise to gradients
#             for param in local_model.parameters():
#                 if param.requires_grad:
#                     # print(param)
#                     noise = torch.tensor(
#                         torch.randn_like(param.grad) * epsilon / num_local_epochs
#                     ).to(device)
#                     param.grad += noise

#             # Update the model parameters
#             optimizer = torch.optim.SGD(local_model.parameters(), lr=lr)
#             optimizer.step()

#         print("Epoch:", epoch, "Loss:", loss.item())

#     return local_model
