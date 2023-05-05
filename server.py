import socket
from _thread import *
from checkers.board import Board
import pickle

server = "192.168.1.39"
port = 5050         # 80 - http

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    pass

s.listen(2)     # number of connections
print("Waiting for connection, Server started")

players = [Board().get_board(), Board().get_board()]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print('Received', reply)
                print('sending', reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Connection lost")
    conn.close()


current_players = 0

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn, current_players))
    current_players += 1
