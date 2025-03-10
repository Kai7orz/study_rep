#stage1
#クライアント側
#--->メッセージを: usernameの長さ+username+メッセー内容
#の形で送信する役割を担う
#入力形式は，必ずusername?から始まって，その後message?
#として，入力後に上記メッセージを作成.(ここで4096バイト以下かチェックするとよりいい)
import socket
import asyncio

def make_connection(token,rname):
    token_length = len(token)
    message = "new user is connecting"    
    entire_message = str(len(rname))+str(len(token))+rname+message
    entire_message = entire_message.encode('utf-8')

    return entire_message


async def make_message(token,rname):

    token_length = len(token)

    message = await asyncio.to_thread(input, "\n input your message: \n")   
    entire_message = str(len(rname))+str(len(token))+rname+message
    entire_message = entire_message.encode('utf-8')

    return entire_message

async def recv_only_message(sock):
    data,_ = await asyncio.to_thread(sock.recvfrom,4096)
    return data


async def recv_message(sock):
    while True:
        data = await recv_only_message(sock)
        recv_message = data.decode('utf-8')
        print(recv_message)

async def tcp_conn():
    try:    
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((address,port))

        sock.connect((server_address,9001))

        print("starting session")
        operation = await asyncio.to_thread(input,"operation 1:create new room 2:join the room")
        operationPayload =  await asyncio.to_thread(input, "input your name (Less than 10 characters) \n")
        room_name = await asyncio.to_thread(input,"input room name to create or join")
        state = 0

        room_name_size = len(room_name)
        print("ope " ,operation," ",operation.encode())
        request_message = int(room_name_size).to_bytes(1,"big")+int(operation).to_bytes(1,"big")+state.to_bytes(1,"big")+len(operationPayload).to_bytes(29,"big")+room_name.encode('utf-8')+operationPayload.encode('utf-8')
        
        first_connect = sock.send(request_message)
        #monitor_recv = asyncio.create_task(recv_message(sock))

        response_data =  sock.recv(4096)
        print(response_data.decode('utf-8'))
        response_token = sock.recv(4096)
        print("Token:",response_token.decode('utf-8'))
        return (response_token.decode('utf-8'),room_name)

    except Exception as e:
        print("close ",e)
        sock.close()

async def send_message(sock,token,rname):

    message_to_send = await make_message(token,rname)
    if message_to_send:
        print("UDP socket sent message  to " ,server_address,server_udp_port )
        sent = sock.sendto(message_to_send,(server_address,server_udp_port))
    else:
        print("nothing to send")


async def udp_conn(token,rname):
    #ソケット生成
    #token付きで，サーバーへデータ送信
    #サーバーが受信して，このトークン，ユーザー，アドレスをアクティブリストに入れておく
    #最初のトークン送信はjoin server としてメッセージを強制的に送信
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((address,port))

    first_connect = sock.sendto(make_connection(token,rname),(server_address,server_udp_port))
    print("sent!")
    monitor_recv = asyncio.create_task(recv_message(sock))

    try:
        while True:
            await send_message(sock,token,rname)
            await asyncio.sleep(1)
    finally:
        sock.close()

    


async def main():
    #ルームへの接続を確立
    token,rname = await tcp_conn()
    await udp_conn(token,rname)

    



address = '127.0.0.2'
port = int(input("enter port (recommended:9002-9010) -->"))
server_address = "localhost"
server_port = 9001
server_udp_port = 9000
asyncio.run(main())    
