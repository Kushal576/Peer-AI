from queue import Queue
from FedAVG import fed_avg_experiment
from flask import Flask, request, jsonify
import time
from base import MLP
import torch

modelList = Queue()





if __name__ == "__main__":
    #     # Start the thread for checking peer availability
#     threading.Thread(target=check_peer_availability).start()
#     # Run Flask app
#     app.run(host='0.0.0.0', port=8000)
    while True:
       time.sleep(10)
       while not modelList.is_empty():
            local_model = modelList.dequeue()
            try:
                global_model = MLP()
                try:
                    global_model.load_state_dict(torch.load('global_model.pth'))
                except:
                    raise Exception("No global model found")
                fed_avg_experiment(global_model, local_model)
                torch.save(global_model.state_dict(), 'global_model.pth')
                print(" Global model updated successfully")
            except:
                modelList.enqueue(local_model)
                raise Exception("Local model update failed. ")



