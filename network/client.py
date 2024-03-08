import requests, csv, json
from model.base import MLP
import torch

def send_model_for_optimization(ip: str, model: MLP):
    # print(str(model.state_dict()))
    torch.save(model, "localmodel.pth")
    files = {'file': open('localmodel.pth', 'rb')}
    resp = requests.post("http://{}/receive_model".format(ip), files=files)
    
    if resp.status_code == 200:
        return True
    
    return False

    