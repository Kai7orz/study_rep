#stage1
#クライアント側
#--->メッセージを: usernameの長さ+username+メッセー内容
#の形で送信する役割を担う
#入力形式は，必ずusername?から始まって，その後message?
#として，入力後に上記メッセージを作成.(ここで4096バイト以下かチェックするとよりいい)
import socket

def make_message():
    username = input('your name ? ---> ')
    username_length = len(username)
    message = input('message to send ? ---> ')
    
    entire_message = str(username_length)+username+message
    entire_message = entire_message.encode('utf-8')

    return entire_message


server_address = "localhost"
server_port = 9001

address = ''
port = int(input("enter port 9001- "))
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((address,port))
while True:
    message_to_send = make_message()
    sent = sock.sendto(message_to_send,(server_address,server_port))

    print('waiting to receive from server ...')

    operation = input('Send any message-->y Waiting for messages--->n ')
    if operation == 'n':
        data,server = sock.recvfrom(4096)
        recv_message = data.decode('utf-8')
        username_length = int(recv_message[0])
        temp_username = recv_message[1:username_length+1]
        temp_message = recv_message[username_length+1:len(recv_message)]
        print('User: ',temp_username,' Message: ',temp_message)

sock.close()