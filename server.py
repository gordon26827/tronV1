import socket
import pickle
from _thread import *
from classes import *

# This port should work for most systems
port = 5555

# Use this IP variable to have socket automatically detect your local IP
ip = socket.gethostbyname(socket.gethostname())

# Alternatively, uncomment line 16 to manually enter your desired IP.
# This is necessary to play with users not connected to the same network as the server
# (in such a case, use your public IP instead)

# ip = "your IP address here"

print(f"Current Server IP: [{ip}]")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))

players = []


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    print(player)

    while True:
        try:
            # int is number of bits being received. Increase to allow for more info to flow at the cost of slower speeds
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break

            conn.sendall(pickle.dumps(players))
        except:
            break

    print("Lost Connection")
    players[player].kill()
    conn.close()


def start():
    num_players = 0
    server.listen(4)
    while True:
        conn, addr = server.accept()
        players.append(Rider(num_players))
        start_new_thread(threaded_client, (conn, num_players))
        num_players += 1


print("Starting server")
start()
