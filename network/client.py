import requests, csv, json
from ..model.base import MLP

file = open("ips")
ips_csv = csv.reader(file)
ips = []
for ip in ips_csv:
    ips.append(ip)
print(ips)

def send_model_for_optimization(model: MLP):
    resp = requests.post("http://20.246.96.203/receive", json={"message": "model", "data": json.loads(model.state_dict())})

    if resp.status_code == 200:
        return True
    
    return False

    