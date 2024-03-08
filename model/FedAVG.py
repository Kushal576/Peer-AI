import os
import torch

def running_model_avg(current, next, scale):
    if current == None:
        current = next
        for key in current:
            current[key] = current[key] * scale
    else:
        for key in current:
            current[key] = current[key] + (next[key] * scale)
    return current


def fed_avg_experiment(global_model, local_model,  num_clients_per_round=4):
    global_model.eval()
    global_model = global_model.to(os.getenv("device"))

    running_avg = running_model_avg(global_model.state_dict(), local_model.state_dict(), 1/num_clients_per_round)
        
    # set global model parameters for the next step
    global_model.load_state_dict(running_avg)


    return global_model


criterion = torch.nn.CrossEntropyLoss()

def validate(model, dataset):
    model = model.to(os.getenv("device"))
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for (t, (x,y)) in enumerate(dataset):
            x = x.to(os.getenv("device"))
            y = y.to(os.getenv("device"))
            out = model(x)
            correct += torch.sum(torch.argmax(out, dim=1) == y).item()
            total += x.shape[0]
    return correct/total