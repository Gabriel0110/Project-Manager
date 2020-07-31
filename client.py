import socket
import pickle

class Client:
    _HOST_IP = '10.0.0.211'
    _PORT = 1234

    def __init__(self):
        self.client_socket = socket.socket()

    def getHostIP(self):
        return Client._HOST_IP

    def getPort(self):
        return Client._PORT

    def connect(self):
        print("Attempting to connect...")
        try:
            self.client_socket.connect((self.getHostIP(), self.getPort()))
            print("CONNECTION SUCCESSFUL!\n")
        except socket.error as e:
            print(str(e))

def main():
    client = Client()
    client.connect()

    response = client.client_socket.recv(1024)
    print(response.decode('utf-8'))
    while True:
        Input = input('Say Something: ')
        client.client_socket.send(str.encode(Input))
        response = client.client_socket.recv(1024)
        print(response.decode('utf-8'))

    client.client_socket.close()

if __name__ == "__main__":
    main()