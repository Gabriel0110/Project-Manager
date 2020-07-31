import socket
import os
import pickle
from functools import partial
from _thread import *
import Database as DB

class Server:
    _HOST_IP = '10.0.0.211'
    _PORT = 1234

    def __init__(self):
        self.server_socket = socket.socket()
        self.thread_count = 0
        self.num_clients = 0
        self.client_dict = {}
        self.session_used_ids = []

    def getHostIP(self):
        return Server._HOST_IP

    def getPort(self):
        return Server._PORT

    def connectThreadedClient(self, connection):
        initial_msg =  " ------------------------------------\n"
        initial_msg += "|        WELCOME TO THE SERVER       |\n"
        initial_msg += " ------------------------------------\n"
        connection.sendall(str.encode(initial_msg))
        client_id = self.getClientID(connection)

        while True:
            # Get data from client
            try:
                data = connection.recv(2048)
            except (ConnectionResetError, ConnectionAbortedError) as e:
                if "WinError 10054" or "WinError 10053" in str(e):
                    print("\n[!] Client {} has disconnected.".format(client_id))
                    break
                else:
                    print(str(e))
                    break

            print("\n[Client {}]: {}".format(client_id, data.decode('utf-8')))
            reply = '[Server]: Client {} said "{}"\n'.format(client_id, data.decode('utf-8'))

            # Attempt to send a response
            try:
                connection.sendall(str.encode(reply))
            except ConnectionAbortedError as e:
                if "WinError 10053" in str(e):
                    print("\n[!] Client {} has disconnected.".format(client_id))
                    break
                else:
                    print(str(e))
                    break

        del self.client_dict[client_id]
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()
        self.thread_count -= 1
        self.num_clients -= 1
        return

    def getID(self):
        idx = 0
        # Get a free ID slot by checking against IDs in database
        while True:
            if idx in self.client_dict.keys() or idx in self.session_used_ids:
                #print("ID already found in client dict -- incrementing before assigning.")
                idx += 1
            else:
                return idx

    def getClientID(self, client):
        for id, info in self.client_dict.items():
            if client in info:
                return id

    def run(self):
        try:
            self.server_socket.bind((self.getHostIP(), self.getPort()))
        except socket.error as e:
            print(str(e))
            return

        print("\n------ SERVER RUNNING ------\n")
        print('[*] Waiting for a connection...\n')
        self.server_socket.listen(5)

        while True:
            client, address = self.server_socket.accept()
            print("\n---------------------------------------------------------")
            print('[!] CONNECTION FROM: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.connectThreadedClient, (client, ))

            client_id = self.getID()
            self.client_dict[client_id] = [client, address]
            self.session_used_ids.append(client_id)
            print("[*] Client with ID {} stored in client dict.".format(client_id))

            self.thread_count += 1
            self.num_clients += 1
            #print('\nThread Number: ' + str(self.thread_count))
            print('[*] Number of clients currently connected: ' + str(self.num_clients))
            print("---------------------------------------------------------\n")

        self.server_socket.close()

def main():
    server = Server()
    server.run()

if __name__ == "__main__":
    main()