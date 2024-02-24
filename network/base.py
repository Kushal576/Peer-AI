import socket
import threading

PORT = 80
class Node:
    """
    Create a Node in the peer-to-peer network 
    """
    def __init__(self,ip : str, list_of_peers: list):
        self.ip = ip
        self.port = PORT
        self.peers = list_of_peers

        # Create a seperate thread for server and start the thread
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()


        # Connect to every peer in the network as a client
        for peer in list_of_peers:
            self.connect_to_peer(peer, PORT)
        

    def handle_client(self, client_socket):
        """Function to handle incoming connections from other peers"""
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print("Received message:", data)

        # Close the connection
        client_socket.close()

    def start_server(self):
        """Function to start the server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(5)
        print("Server started, listening on port {}".format(self.port))

        while True:
            client_socket, client_addr = server.accept()
            print("Accepted connection from:", client_addr)

            if client_addr not in self.peers:
                self.peers += client_addr
                self.connect_to_peer(client_addr[0], client_addr[1])

            # Start a new thread to handle the client
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            
            client_handler.start()

    def connect_to_peer(self, peer_ip, peer_port):
        """Function to connect to another peer"""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((peer_ip, peer_port))
        print("Connected to peer at {}:{}".format(peer_ip, peer_port))

        # Send a message to the peer
        while True:
            message = input("Enter message to send (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client.send(message.encode('utf-8'))

        # Close the connection
        client.close()

if __name__ == "__main__":

    # Connect to other peers
    node = Node()
    while True:
        peer_ip = input("Enter peer IP address to connect to (type 'exit' to quit): ")
        if peer_ip.lower() == 'exit':
            break
        peer_port = int(input("Enter peer port: "))
        node.connect_to_peer(peer_ip, peer_port or 1025)