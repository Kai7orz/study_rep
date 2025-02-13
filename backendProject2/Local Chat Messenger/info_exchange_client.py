import socket
import os 
from faker import Faker

#client,server作成の流れはおなじで流すデータだけ変えればよい


fake = Faker()

sock = socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM)

server_address = '/tmp/server_address'
client_address = '/tmp/client_address'

try:
    os.unlink(client_address)
except FileNotFoundError:
    pass


sock.bind(client_address)

message = "User Name ::" + fake.name() + " User Address ::" + fake.address()
message = message.encode('utf-8')
try:
    sent = sock.sendto(message,server_address)
    
    print('waiting response from server')
    data,server = sock.recvfrom(4096)
    print('Received message {} from server'.format(data))

finally:
    print('Sending is finised')
