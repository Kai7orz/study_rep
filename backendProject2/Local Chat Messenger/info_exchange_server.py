import os 
import socket 

sock = socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM)

server_address = '/tmp/server_address'

try:
    os.unlink(server_address)
except FileNotFoundError as e:
    print(e)
    pass
sock.bind(server_address)

while True:
    data,address = sock.recvfrom(4096)

    if data:
        response_message = 'server recieved {} .This is Ack message '.format(data)
        response_message = response_message.encode('utf-8')
        sent = sock.sendto(response_message,address)
        print('sent {} bytes back to {}'.format(sent,address))