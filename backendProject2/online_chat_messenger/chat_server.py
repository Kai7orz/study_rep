#stage1
#サーバー側
# -----接続の確立-------
# 1.プログラム開始
# 2.ソケットの生成
# 3.usernameの認識
# 4.usernameがすでに登録されたものか判断して，されていなければ新たに登録.されていれば，最終メッセージ送信時刻の更新
# 5.message_buffer[username]に対して，送信されたメッセージをappend
# 6.送信されたメッセージを登録リストに対応した(address，port)に送信 

# manage_userメソッド 登録されたユーザに対して，最終接触時刻と現在時刻の差が一定値以上であれば，登録リストおよびそのユーザのmessage_bufferを削除(n秒に1回の頻度)
# (機能要件の何回か連続で失敗するか、しばらくメッセージを送信していない場合　というのは，サーバー側から見れば，どちらも一定時間以上メッセージを受信しないという条件にまとめていい？？)

#データ構造:
# address_port: キー:username 値:(address,port)
# message_buffer: キー:username 値:["message1",message2",...]
# last_contact: キー:username 値: 最終メッセージ送信時刻

#関数・クラス
#  class user: メンバーに address,port,message_buffer, last_contact を持ち，メソッドにupdate_userを持つ.これはメッセージ受信時に呼ばれる.
#　class  server:メンバーにuser_list=[user1,user2,...] を持ち，メソッドにstart,manage_userをもつ

import socket
import  time

para_t = 10

class user:
    #last_contact はtime.time()入る想定
    def __init__(self,address,port,username,message_buffer,last_contact):
        self.address = address
        self.port = port 
        self.username = username
        self.message_buffer = message_buffer
        self.last_contact = last_contact

    def update_user(self):
        self.last_contact = time.time()

class server:
    def __init__(self,server_address,server_port,sock,user_list=[]):
        self.server_address = server_address
        self.server_port = server_port
        self.sock = sock
        self.user_list = []
    
    def is_new_user(self,temp_username):
        for one_user in self.user_list:
            if temp_username == one_user.username:
                return False
        return True

    def manage_user(self):
        active_users = [u for u in self.user_list if (time.time() - u.last_contact) < para_t]
        self.user_list = active_users 

    def show_client_list(self):
        print("------------clients--------------")
        for u in self.user_list:
            print("user:",u.username)
 
    
    def start(self):


        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("socket created successfully")
        except OSError as e:
            print("socket creation failed", e)

        self.sock.bind((self.server_address,self.server_port))
           
        while True:
            client_data,client_address_port = self.sock.recvfrom(4096)
            client_raw_data = client_data
            client_data = client_data.decode('utf-8')           
            if client_data:
                username_length = int(client_data[0])
                temp_username = client_data[1:username_length+1]
                temp_message = client_data[username_length+1:len(client_data)]
                print("server received from ",temp_username," message: ",temp_message)

                #user名が登録済みの者かどうか判定する関数bool
                #リストになければ新たに登録する
                #すでに登録されていれば，最終送信時刻の更新
                if self.is_new_user(temp_username):
                    buf = [temp_message]
                    new_user = user(client_address_port[0],client_address_port[1],temp_username,buf,time.time())
                    self.user_list.append(new_user)

                else:
                    for u in self.user_list:
                        if temp_username == u.username:
                            u.update_user() 
                            u.message_buffer.append(temp_message) #メッセージの保存

                #ここからメッセージを，接続が確立しているノードに対して送信する
                #ここでuserの管理してから送信
                self.manage_user()
                self.show_client_list()
                for client in self.user_list:
                    if client.username != temp_username:
                        print("server sent data to ",client.username)        
                        sent = self.sock.sendto(client_raw_data,(client.address,client.port))
                





server_address = '0.0.0.0'
server_port = 9001
sock = None
user_list = []

try:
    my_server = server(server_address,server_port,sock,user_list)
    my_server.start()
finally:
    sock.close()









                



