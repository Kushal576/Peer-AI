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

# Store information about peers
peers = {
    "training":["20.121.57.95:80", "20.121.62.226:80", "172.203.99.79:80", "172.208.98.225:80"],
    # "training":["192.168.206.177:8000"],
    "aggregating":["20.186.56.9:80"],
    "verification":set(),
    "other":set()
}

# epoch = 5
# lr = 1e-3
sleep_time = 20

mlp = base.MLP()
# global_model = copy.deepcopy(mlp)
modelList = Queue()

def enqueue_model_list(model):
    modelList.enqueue(model)
    return True

def training(global_model, optim = torch.optim.SGD, lr = 1e-3, epoch = 5):
    dataset = torch.load(str(_dataset))
    pth = os.path.exists('global_model.pth')

    if pth:
        global_model.load_state_dict(torch.load('global_model.pth'))

    local_model = train_client(dataset, global_model=global_model, num_local_epochs=epoch,lr =lr, optim = optim)
    acc = validate(local_model, dataset)

    send_model_for_optimization(peers['aggregating'][0],local_model)
    print(acc)
    time.sleep(sleep_time)

    return acc

max_iter = 20
local_accuracy = {
    "dataloader_0.pth":[],
    "dataloader_1.pth":[],
    "dataloader_2.pth":[],
    "dataloader_3.pth":[],
}

def traininig_test(dataset, name):
    for i in range(max_iter):
        print(f"{i}: {name}")
        global_model = copy.deepcopy(mlp)
        pth = os.path.exists('global_model.pth')
        if pth:
            global_model.load_state_dict(torch.load('global_model.pth'))

        local_model = train_client(dataset, global_model=global_model, num_local_epochs=5,lr =1e-3, optim = torch.optim.SGD)
        acc = validate(local_model, name)
        local_accuracy[name].append(acc)
        modelList.enqueue(local_model)
        aggregating()
        print(modelList.items)
        np.save("accuracy" + str(name), local_accuracy[name])

    return True
accuracy = []
training_acc = []

def aggregating():
    round = 0
    #    time.sleep(10)
    global_model2 = copy.deepcopy(mlp)
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
                # acc = validate(global_model3)
                # acc2 = validate(global_model3, "dataloader_full.pth")
                # accuracy.append(acc)
                # training_acc.append(acc2)
                torch.save(global_model3.state_dict(), 'global_model.pth')
                for ip in peers['training']:
                    send_model_for_optimization(ip, global_model3)
                print(" Global model updated successfully")

            except:
                modelList.enqueue(local_model)
                raise Exception("Local model update failed. ")
            
            round +=1

            # np.save(f"validation_accuracy_{round}.npy", np.array(accuracy))
            # np.save("training_accuracy_glob.pth", np.array(training_acc))



def train_test(global_model):
    accuracy = []


    for i in range(10):
        ith = random.randint(0,3)
        traininig_test("dataloader_{}.pth".format(ith), global_model= global_model)
        global_model, acc = aggregating()
        accuracy.append(acc)
        print("Epoch : {} \n dataset {} \t Model Accuracy: {}".format(i,ith, acc))


    np.save('accuracy.npy+', np.array(accuracy))
    

def train(optimizer, lr, epoch):
    global_model = copy.deepcopy(mlp)
    accuracy = []
    for i in range(10):
        acc = training(global_model, optim=optimizer, lr = lr, epoch = epoch)
        accuracy.append(acc)
        # print(acc)
        np.save("accuracy_{}.npy".format(str(i)), acc)

    np.save("accuracy_final.npy", accuracy)
    print(accuracy)


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
