import socket
import threading
#クライアント　送信と受信をマルチスレッドで対応する

class user:
    def __init__(self):
        self.user_name = None 
        self.message = None
        self.sever_address = None
        self.udp_socket = None


    def start_session(self):
        #udpソケットの生成とサーバip,port入力
        #server_ip = input("server address ?")
        #server_port = input("server port?")

        server_ip = "127.0.0.1"
        server_port = 9000

        self.server_address = (server_ip,int(server_port))
        self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #socket の生成
        
        thre = threading.Thread(target = self.receive_message)
        thre.start()
        
        self.user_name = input("input your user name ") 
        
    def make_message(self):
        tmp_message = input("enter your message ")
        user_name_length = len(self.user_name)#user name の長さを1バイトに変換（big endian）
        print("client_name_length:",user_name_length)
        self.message = user_name_length.to_bytes(1,'big') + self.user_name.encode('utf-8')+ tmp_message.encode('utf-8')

    def receive_message(self):
        while True:
           message,s_addr = self.udp_socket.recvfrom(4096)
           print("receive message from server :",message.decode('utf-8'))

    def send_message(self):
        while True:
            try:    
                    print("Ctrl + c to finish session")
                    self.make_message()
                    send_length = self.udp_socket.sendto(self.message,self.server_address)
            except KeyboardInterrupt:
                print("close socket")
                self.udp_socket.close()
                print("Done")
                break


def main():
    my_client = user()
    my_client.start_session()
    my_client.send_message()



if __name__ == "__main__":
    main()