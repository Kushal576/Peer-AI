import copy, os, dotenv, torch, requests
from . import base
from .train import train_client
from .FedAVG import fed_avg_experiment, validate
import time, random
from .queue import Queue
import numpy as np
from ..network.client import send_model_for_optimization


dotenv.load_dotenv(".env")
_type = os.getenv("TYPE")
_dataset = os.getenv("DATASET_PATH")


epoch = 10
lr = 1e-3
sleep_time = 20

mlp = base.MLP()
# global_model = copy.deepcopy(mlp)
modelList = Queue()

def training(global_model):
    dataset = torch.load(str(_dataset))
    pth = os.path.exists('global_model.pth')

    if pth:
        global_model.load_state_dict(torch.load('global_model.pth'))

    local_model = train_client(dataset, global_model=global_model, num_local_epochs=epoch,lr =lr, optim = torch.optim.SGD)
    send_model_for_optimization(local_model)
    time.sleep(sleep_time)




def traininig_test(_dataset_, global_model):
    dataset = torch.load(str(_dataset_))
    local_model = train_client(dataset, global_model=global_model, num_local_epochs=epoch,lr =lr, optim = torch.optim.SGD)
    modelList.enqueue(local_model)


def aggregating():
    #    time.sleep(10)
    global_model2 = copy.deepcopy(mlp)
    accuracy = None
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
            accuracy = validate(global_model3)

            torch.save(global_model3.state_dict(), 'global_model.pth')

            print(" Global model updated successfully")

        except:
            modelList.enqueue(local_model)
            raise Exception("Local model update failed. ")
    return global_model3, accuracy
            


def train_test(global_model):
    accuracy = []


    for i in range(10):
        ith = random.randint(0,3)
        traininig_test("dataloader_{}.pth".format(ith), global_model= global_model)
        global_model, acc = aggregating()
        accuracy.append(acc)
        print("Epoch : {} \n dataset {} \t Model Accuracy: {}".format(i,ith, acc))


    np.save('accuracy_.npy+', np.array(accuracy))




def main():
    if str(_type) == "training":

        training()

    if str(_type) == "aggregating":
        global_model = copy.deepcopy(mlp)
        train_test(global_model=global_model)
        pass