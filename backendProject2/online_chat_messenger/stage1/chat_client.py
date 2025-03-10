#stage1
#クライアント側
#--->メッセージを: usernameの長さ+username+メッセー内容
#の形で送信する役割を担う
#入力形式は，必ずusername?から始まって，その後message?
#として，入力後に上記メッセージを作成.(ここで4096バイト以下かチェックするとよりいい)
import socket
import asyncio


def make_connection(username):
    username_length = len(username)
    message = "new user is connecting"    
    entire_message = str(username_length)+username+message
    entire_message = entire_message.encode('utf-8')

    return entire_message

async def make_message(username):
    username_length = len(username)
    message = await asyncio.to_thread(input, "\n input your message: \n")
    
    entire_message = str(username_length)+username+message
    entire_message = entire_message.encode('utf-8')

    return entire_message

async def recv_only_message(sock):
    data,_ = await asyncio.to_thread(sock.recvfrom,4096)
    return data


async def recv_message(sock):
#    data,server = await sock.recvfrom(4096)
    while True:
        data = await recv_only_message(sock)
        recv_message = data.decode('utf-8')
        username_length = int(recv_message[0])
        temp_username = recv_message[1:username_length+1]
        temp_message = recv_message[username_length+1:len(recv_message)]
        print('-----------------------------------------------')
        print('User: ',temp_username,' Message: ',temp_message)
        print('-----------------------------------------------')
        print('\n input your message: ')

async def send_message(sock,username):
    message_to_send = await make_message(username)
    if message_to_send:
        sent = sock.sendto(message_to_send,(server_address,server_port))
    else:
        print("nothing to send")

async def main():
    address = ''
    port = int(input("enter port (recommended:9002-9010) -->"))
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((address,port))
    
    print("starting session")
    username = await asyncio.to_thread(input, "input your name (Less than 10 characters) \n")
    if len(username) >= 10:
        print("Name Length Error")
        sock.close()
        exit()

    first_connect = sock.sendto(make_connection(username),(server_address,server_port))
    monitor_recv = asyncio.create_task(recv_message(sock))
    try:
        while True:
            await send_message(sock,username)
            await asyncio.sleep(1)
    finally:
        sock.close()


server_address = "localhost"
server_port = 9001
asyncio.run(main())    