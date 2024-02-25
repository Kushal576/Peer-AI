import requests, csv, json
from model.base import MLP
import torch

file = open("ips")
ips_csv = csv.reader(file)
ips = []
for ip in ips_csv:
    ips.append(ip)
print(ips)

def send_model_for_optimization(ip: str, model: MLP):
    # print(str(model.state_dict()))
    torch.save(model, "localmodel.pth")
    files = {'file': open('localmodel.pth', 'rb')}
    resp = requests.post("http://{}/receive_model".format(ip), files=files)
    
    if resp.status_code == 200:
        return True
    
    return False

    