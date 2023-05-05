import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.39"
        self.port = 5050
        self.addr = (self.server, self.port)
        self.p = self.connect()
        self.id = 0

    def get_p(self):
        return self.p

    def get_player_number(self):
        return self.id

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048*2))
        except pickle.PickleError as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            received_data = self.client.recv(2048*2)
            while not received_data:
                received_data = self.client.recv(2048*2)
            return pickle.loads(received_data)
        except socket.error as e:
            print(e)

