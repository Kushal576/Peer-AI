from flask import Flask, request, jsonify
import requests
import threading
import time
import copy, os, dotenv, torch
from model.base import MLP
from model.__main__ import enqueue_model_list
import uuid
app = Flask(__name__)

# Store information about peers
peers = {
    "training":set(),
    "verification":set(),
    "aggregation":set(),
    "other":set()
}

messages = []

# Function to send message to all peers
def send_message_to_all(message):
    try:
        for _peer in peers:
            print(_peer)
            for peer in peers[_peer]:
                requests.post("http://" + peer + "/receive", json={"message": message})
    except:
        raise Exception("Message send Failed")

# Endpoint to receive messages
@app.route('/receive', methods=['POST'])
def recv1():
    message = request.json.get('message')

    if message =="global_model":
        data = request.json.get('data')

        
        model = MLP()
        model.load_state_dict(data)
        torch.save(model, "global_model.pth")
    # messages.append(message)
    return jsonify({"status": "Message received"})

@app.route('/receive_model', methods=['POST'])
def receive_model():
    model = request.files['file']
    if os.getenv('TYPE') == 'aggregation':
        model_uuid = uuid.uuid4()
        if not os.path.exists('localmodels'):
            os.mkdir('localmodels')
        model.save(f'localmodels/localmodel_{model_uuid}.pth')
        _model = torch.load(f'localmodels/localmodel_{model_uuid}.pth')
        enqueue_model_list(_model)
    else:
        model.save('globalmodel.pth')
    
    return jsonify({"status":"Model Received."})

# Endpoint to send message to all peers
@app.route('/send_to_all', methods=['POST'])
def send_to_all():
    message = request.json.get('message')
    send_message_to_all(message)
    return jsonify({"status": "Message sent to all peers"})

# # Endpoint to send message to a specific peer
@app.route('/send_to_peer', methods=['POST'])
def send_to_peer():
    peer = request.json.get('peer')
    message = request.json.get('message')
    requests.post("http://" + peer + "/receive", json={"message": message})
    return jsonify({"status": "Message sent to peer"})

def send_message(peer: str, message: str):
    """
    peer : str :- IP:PORT of the peer to send the message
    message : str :- Message to be sent to the peer
    """
    try:
        requests.post("http://" + peer + '/receive', json={"message": message})
    except:
        raise Exception("Sending message to peer failed.")
    return True

def message_broadcast(message : str, _type : str):
    """
    message : str :- message to be broadcasted to the peer network
    _type : str :- type of peers to broadcast the message, 'all' if to be broadcasted for 
                    every peer in the network
    """
    try:
        for _peer in (peers if _type == 'all' else peers[str(_type)]):
            for peer in peers[_peer]:
                send_message(peer, message)
    except:
        raise Exception("Message Broadcast Failed")

# Endpoint to join the peer network
@app.route('/join', methods=['POST'])
def join_network():
    peer = request.json.get('peer')
    _type = request.json.get('type')
    print(request.environ['SERVER_NAME'])
    dotenv.load_dotenv(".env")
    own_ip = os.getenv("IP")
    own_port = os.getenv("PORT")
    own_type = os.getenv("TYPE")
    print(own_ip)
    # send join request to peer
    if peer not in peers[str(_type)]:
        peers[str(_type)].add(peer)
        resp = requests.post("http://" + peer + "/join", json={"peer": str(own_ip) +  ":"+ str(own_port), "type": str(own_type)})
        if resp.status_code != 200:
            return jsonify({"status": "Error while adding peer"})


    # print(peers)

    return jsonify({"status": "Peer added to the network"})


# Function to periodically check peer availability
def check_peer_availability():
    """
    uses ping functionality of the server
    """
    while True:
        time.sleep(10)
        _peers = copy.deepcopy(peers['verification'])

        for peer in _peers:
            try:
                response = requests.get("http://" + peer + "/ping")
                if response.status_code != 200:
                    peers["verification"].remove(peer)
                    print(f"{peer} removed from network")
            except:
                peers["verification"].remove(peer)
                print(f"{peer} removed from network")

        _peers = copy.deepcopy(peers['aggregation'])
        for peer in _peers:
            try:
                response = requests.get("http://" + peer + "/ping")
                if response.status_code != 200:
                    peers["aggregation"].remove(peer)
                    print(f"{peer} removed from network")
            except:
                peers["aggregation"].remove(peer)
                print(f"{peer} removed from network")


        _peers = copy.deepcopy(peers['training'])
        for peer in _peers:
            try:
                response = requests.get("http://" + peer + "/ping")
                if response.status_code != 200:
                    peers["training"].remove(peer)
                    print(f"{peer} removed from network")
            except:
                peers["training"].remove(peer)
                print(f"{peer} removed from network")


        _peers = copy.deepcopy(peers['other'])
        for peer in _peers:
            try:
                response = requests.get("http://" + peer + "/ping")
                if response.status_code != 200:
                    peers["other"].remove(peer)
                    print(f"{peer} removed from network")
            except:
                peers["other"].remove(peer)
                print(f"{peer} removed from network")

# Endpoint for peers to ping and check availability
@app.route('/ping', methods=["GET"])
def ping():
    """
    returns status = OK if gets message
    required to check if the server is online
    """
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    # Start the thread for checking peer availability
    threading.Thread(target=check_peer_availability).start()
    # Run Flask app
    app.run(host='0.0.0.0', port=8000)
