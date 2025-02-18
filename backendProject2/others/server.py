import socket 
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001
print('starting up on port {}'.format(server_port))

sock.bind((server_address,server_port))

while True:
    print("\n waiting to receive message ...")
    data,address = sock.recvfrom(4096)
    print('received {} bytes from {} '.format(len(data),address))
    print(data)

    if data:
        sent = sock.sendto(data,address)
        print('sent {} bytes back to {}'.format(sent,address))