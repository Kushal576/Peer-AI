import copy, os, dotenv, torch, requests
from . import base
from .train import train_client
from .FedAVG import fed_avg_experiment, validate
import time, random
from .queue import Queue
import numpy as np
from network.client import send_model_for_optimization


dotenv.load_dotenv(".env")
_dataset = os.getenv("DATASET_PATH")


epoch = 10
lr = 1e-3
sleep_time = 0

mlp = base.MLP()
# global_model = copy.deepcopy(mlp)
modelList = Queue()
training_ips = ["20.121.57.95:80", "20.121.62.226:80", "172.208.98.225:80", "172.203.99.79:80"]

def enqueue_model_list(model):
    modelList.enqueue(model)
    return True

def training(global_model):
    dataset = torch.load(str(_dataset))
    pth = os.path.exists('global_model.pth')

    if pth:
        global_model.load_state_dict(torch.load('global_model.pth'))

    local_model = train_client(dataset, global_model=global_model, num_local_epochs=epoch,lr =lr, optim = torch.optim.SGD)
    acc = validate(local_model, "dataloader_0.pth")

    send_model_for_optimization('192.168.241.11:8000',local_model)
    time.sleep(sleep_time)

    return acc




def traininig_test(_dataset_, global_model):
    dataset = torch.load(str(_dataset_))
    local_model = train_client(dataset, global_model=global_model, num_local_epochs=epoch,lr =lr, optim = torch.optim.SGD)
    modelList.enqueue(local_model)


def aggregating():
    #    time.sleep(10)
    global_model2 = copy.deepcopy(mlp)
    accuracy = []
    round=0
    print("Run Main Here")
    while True:
        while not modelList.is_empty():
            local_model = modelList.dequeue()
            try:

                pth = os.path.exists('global_model.pth')

                if pth:
                    global_model2.load_state_dict(torch.load('global_model.pth'))
                # try:
                # except:
                global_model3 = fed_avg_experiment(global_model=global_model2, local_model=local_model)
                #     raise Exception("No global model found")
                acc = validate(global_model3)
                accuracy.append(acc)
                torch.save(global_model3.state_dict(), 'global_model.pth')
                for ip in training_ips:
                    send_model_for_optimization(ip, global_model3)
                print(" Global model updated successfully")

            except:
                modelList.enqueue(local_model)
                raise Exception("Local model update failed. ")
            
            round +=1

            np.save(f"accuracy_{round}.npy", np.array(accuracy))


            


def train_test(global_model):
    accuracy = []


    for i in range(10):
        ith = random.randint(0,3)
        traininig_test("dataloader_{}.pth".format(ith), global_model= global_model)
        global_model, acc = aggregating()
        accuracy.append(acc)
        print("Epoch : {} \n dataset {} \t Model Accuracy: {}".format(i,ith, acc))


    np.save('accuracy.npy+', np.array(accuracy))




def main():
    if str(os.getenv('TYPE')) == "training":
        global_model = copy.deepcopy(mlp)
        accuracy = []
        for i in range(10):
            acc = training(global_model)
            accuracy.append(acc)
            print(acc)
        print(accuracy)

    if str(os.getenv('TYPE')) == "aggregation":
        global_model = copy.deepcopy(mlp)
        aggregating()
                    
# main()
