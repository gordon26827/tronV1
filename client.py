import socket
import pickle

header = 64
port = 5050
ip = socket.gethostbyname(socket.gethostname())
addr = (ip, port)
format = 'utf-8'
disconnect = 'disconnect'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

def send(msg):
    message = msg.encode(format)
    msg_length = len(message)
    send_length = str(msg_length).encode(format)
    send_length += b' ' * (header - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048))

send("Hello!!!")
send(disconnect)