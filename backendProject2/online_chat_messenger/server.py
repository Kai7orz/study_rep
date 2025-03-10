import socket 
import time
import threading

class server:
    def __init__(self):
        self.active_clients = []
        self.udp_socket = None
        self.user_send_time = [] #(client_address,message_send_time)
        self.server_address = ("127.0.0.1",9000)

    def is_new_user(self,client_address):
        if client_address in self.active_clients: #クライアントが登録されているか
            return False
        else:
            return True

    def transfer_message(self,message,client_address):
        print("active_clients : ",self.active_clients)
        for user in self.active_clients:
            print("user:",user)
            if client_address != user :
                print("sent to :",user)
                self.udp_socket.sendto(message,user) 
    
    def receive_message(self):
       message_size = 4096
       while True:
            try:
                message,client_address = self.udp_socket.recvfrom(message_size)
                self.user_send_time.append((client_address,time.time()))    #userがメッセージを送信した最終時刻を記録する

                user_name_length = message[0] #messageの1バイト目はuser name の長さで，byteから数値に変換する
                print("user_name_length :",user_name_length)
                user_name = message[1:1+user_name_length].decode('utf-8')
                message_body = message[1+user_name_length:len(message)].decode('utf-8')
                
                if(self.is_new_user(client_address)):     #登録されていないユーザなら登録する
                    self.active_clients.append((client_address))
                
                print("server receive from client:",client_address," user name:",user_name," message:",message_body)

                self.transfer_message(message,client_address)

            except KeyboardInterrupt:
                self.udp_socket.close()
                break

    def manage_user(self):
        print("manage user called ")
        limited_time = 30
        current_time = time.time()
        print("user_send_time:",self.user_send_time)

        delete_clients = [ addr for addr, t in self.user_send_time if (current_time - t) >= limited_time]

        print("delete_clients:",delete_clients)

        self.active_clients = [client for client in self.active_clients if not(client in delete_clients)]
        print("active_clients",self.active_clients)

    def scheduler(self):
        while True:
            self.manage_user()
            time.sleep(5)

    

    def start(self):
        self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udp_socket.bind(self.server_address)
        t = threading.Thread(target = self.scheduler)
        t.start()

def main():
    my_server = server()
    my_server.start()
    my_server.receive_message()

if __name__ == "__main__":
    main()