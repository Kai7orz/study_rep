#stage2
#サーバー側がユーザの名前を受け取って利用する名前をトークンに埋め込む

#サーバー側
# -----接続の確立-------
# 1.プログラム開始
# 2.ソケットの生成 --->>TCPソケットに変更
# 3.RoomNameSize+Operation+State+OperationPayloadSize の受け取り.最初にOperation を読みこんで処理分岐
# --->>>3.1 operation == 1:トークンに使うユーザー名に重複あればエラー返して終了　なければ　　ルーム作成しserverへ登録
#---->>>::Roomクラス(user_list,host,(messagebuffer))を作成し　ユーザへトークンを渡す.
# --->>>3.2 operation == 2: 3.1と同様にトークンに使うユーザー名に重複あればエラー返して終了　なければ　　room名に対応した
#---->>>::Roomクラス(user_list(or token_list)host,(messagebuffer))のhost以外へトークンを登録して　ユーザへトークンを渡す.個のトークンはIPアドレスと一致させる.

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
import asyncio
####テスト####
#①最初のテスト項目は hostのメッセージ送信・serverが受け取った時にroomの作成とtoken追加を問題なく行えるかどうか


para_t = 100


class user:
    #last_contact はtime.time()入る想定
    def __init__(self,user_socket,username,message_buffer,last_contact):
        self.user_socket = user_socket
        self.username = username
        self.message_buffer = message_buffer
        self.last_contact = last_contact

    def update_user(self):
        self.last_contact = time.time()


class room:
    def __init__(self,host,room_name,user_list=[],user_token_map={},token_address_map={}):
        #1度ログインのためにtoken利用したら，リストから削除したほうがセキュリティ上安全
        self.host = host
        self.room_name = room_name
        self.user_list = user_list.append(self.host.username)
        self.user_token_map = user_token_map # 
        self.token_address_map = token_address_map

    def generate_token(self,user,address_port):
        #この関数がuser_token_mapにuserとtokenを追加する責任を負っている.
        #このtokenを管理するmapは{user:token}であることに注意する.　{username:token}ではないことに注意
        #クライアントのアドレスをtokenに埋め込む必要があるけど，どのようにしてクライアントのaddressを取得するかを考える必要がある
        if user == self.host:
            tkn = "host_token"+user.username
            self.user_token_map[user] = tkn
            self.token_address_map[tkn]=address_port
            print("generated token :",tkn.encode('utf-8'))
            return tkn.encode("utf-8")
        else:        
            tkn = str(address_port)
            self.user_token_map[user] = tkn
            self.token_address_map[tkn]=address_port
            return tkn.encode("utf-8")

    #ルーム内のアクティブユーザを管理する.セッションを離脱したユーザlistを返す.
    def manage_user(self):

        active_users = [u for u in self.user_list if (time.time() - u.last_contact) < para_t]
        deleted_users = [deleted_user for deleted_user in self.user_list if (time.time() - deleted_user.last_contact) >= para_t]

        temp_user_list = {}
        for  u in active_users:
            temp_user_list[u] = self.user_token_map[u]

        self.user_token_map = temp_user_list
        self.user_list = active_users 
        return deleted_users

    #ルームに参加するユーザとその対応したトークンを入力として受け取る.
    def add_user(self,user,token):
        self.user_list.append(user)
        self.user_token_map[user] = token

    #ルームに参加するためのトークンをuserが所持しているか
    def can_user_join(self,token):
        for v in self.user_token_map.values():
            if v==token:
                #delete this token from map ?? トークンの使いまわしできないようにするにはこのコード有効化したほうがいいかも
                return True
        return False


"""    
    def is_new_user(self,temp_username):
        for one_user in self.user_list:
            if temp_username == one_user.username:
                return False
        return True

    def show_client_list(self):
        print("------------clients--------------")
        for u in self.user_list:
            print("user:",u.username)

serverは，startしたら，他のクライアントからの接続を受付.
そして，接続確立後にメッセージを受信する.

メッセージのoperation が1なら，roomインスタンスを作成して，
generate_token 呼び出して，ホストのトークンを返してもらう.そして，そのトークンをクライアントへ送信する.

operation が2なら，クライアントのトークンが正しいかの判定を行って，正しければ，rooｍへエンターさせて
，roomにメンバー登録して，クエリをroomからもらいクエリをクライアントへ送信.



tokenの管理方法について考える必要がある

token の生成:
と
tokenの管理:tokenを消費してroomに参加しているuser_listに追加するパターンと
token_listに合致しているかだけ確認するパターン


"""

class server:
    def __init__(self,server_address,server_port,sock,udp_sock,room_list=[]):
        self.server_address = server_address
        self.server_port = server_port
        self.sock = sock
        self.udp_sock = udp_sock
        self.room_list = room_list


    
    def check_client(self,client_room_name,client_token,client_address_port):
        room_flag = False
        token_flag = False
        for r in self.room_list:
            if client_room_name == r.room_name:
                room_flag = True           
                for token in r.user_token_map.values():
                    if token == client_token:
                        token_flag = True
                        if str(r.token_address_map[token]) == str(client_address_port):
                            return True
        return False
            

    async def recv_only_message(self,sock):
        print("recvonly")
        data,address = await asyncio.to_thread(sock.recvfrom,4096)
        print("recv",data)
        return data,address 
    
    async def start_udp(self):
        #udpソケットの作成
            print("Udp socket start setting....")
            self.udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            print("udp bind at ",self.server_address,server_udp_port)
            self.udp_sock.bind((self.server_address,server_udp_port))
            try:
                while True:
                    client_data,client_address_port = await self.recv_only_message(self.udp_sock)
                    client_data = client_data.decode('utf-8')

            
                    if client_data:
                        client_room_name_size = int(client_data[0])
                        client_token_length = int(client_data[1])
                        client_room_name = client_data[2:2+client_room_name_size]
                        client_token = client_data[2+client_room_name_size:2+client_room_name_size+client_token_length]
                        client_message = client_data[2+client_room_name_size+client_token_length:len(client_data)] 
                        print(client_room_name_size,client_room_name,client_token,client_message)                    
                        #room名の存在，そのルーム内に登録されたトークンと受信したトークンが一致するか，そのトークンとipアドレスの対応が適当かチェック
                        if self.check_client(client_room_name,client_token,client_address_port):
                            for target_room in self.room_list:
                                    for user in target_room.user_list:
                                        if str(target_room.user_token_map[user.username]) != str(client_token): 
                                            sent = self.sock.sendto(client_message,user.token_address_map[user.username])
            
            except Exception as e:
                print(e)
                self.udp_sock.close()

    async def start_tcp(self):
        #TCPソケットの作成
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("socket created successfully")
        except OSError as e:
            print("socket creation failed", e)


        #バインド
        self.sock.bind((self.server_address,self.server_port))
        self.sock.listen()
        try:
            while True:
                #ここでawait ?????????
                client,addr = self.sock.accept()
                data,_ = self.recv(4096) #とりあえずテストデータで試してみる
                
                print(data)
                if data:      
                        #最初にheaderを取り除く
                        room_name_size = data[0]
                        operation = data[1]
                        state = data[2]
                        operation_payload_size = int.from_bytes(data[3:32],"big")

                        #次にbodyを取り除く
                        body = data[32:len(data)].decode('utf-8')
                        
                        print(room_name_size,operation,state,operation_payload_size)
                        print(body)

                        
                    
                        if operation == 1:
                            #リクエスト処理OK をクライアントに伝達 + 新しいルームの作成
                            #リクエスト処理返答
                            response_message = "OK".encode("utf-8")
                            #response_sent = self.sock.send(response_message)
                            response_sent = client.sendall(response_message)
                            #bodyの読み
                            room_name = body[32:32+room_name_size]  
                            user_name = body[32+room_name_size:32+room_name_size+operation_payload_size]

                            #host userの作成 def __init__(self,conn(socket object),username,message_buffer,last_contact):
                            host_user = user(client,user_name,message_buffer=[],last_contact=time.time())

                            #新しいルームの作成
                            #room(host,room_name,user_list,token_list,user_token_map):
                            new_room = room(host_user,room_name,user_list=[],user_token_map={},token_address_map={})
                            address  =  addr
                            host_token_data = new_room.generate_token(host_user,address)
                            #新しいルーム作成時serverのroom_listを更新する
                            self.room_list.append(new_room)
                            #client(host)に対して生成したtokenを渡す
                            host_token_sent = client.sendall(host_token_data)
                            print("close1")
                            client.close()
                            print("close2")

                        elif operation == 2:
                        #チャットルームへの参加に関する操作
                        #userの作成と　room へのuserの追加　tokenの作成
                        #リクエスト処理OK をクライアントに伝達 + 新しいルームの作成
                            #リクエスト処理返答
                            response_message = "OK".encode("utf-8")
                            response_sent = client.sendall(response_message)
                            #bodyの読み
                            r_name = body[32:32+room_name_size]  
                            user_name = body[32+room_name_size:32+room_name_size+operation_payload_size]

                            #userが参加したいルームの取得を行なう　なければエラーを出す
                            for r in self.room_list:
                                if(r.room_name == r_name):
                                    target_room = r
                            
                            #参加userの作成 def __init__(self,conn(socket object),username,message_buffer,last_contact):
                            participant_user = user(client,user_name,message_buffer=[],last_contact=time.time())
                            user_address = addr
                            #user用のtoken生成および配布
                            user_token_data = target_room.generate_token(participant_user,user_address)
                            #roomのuserlistに追加
                            
                            user_token_sent = self.sock.send(user_token_data)

                            #roomはtokenの管理を行う責任があるけど，tokenのリストへの追加は，generate_tokenに行われるべきで，削除はmanage_userで行う
                            #token とユーザのマップ更新も同じくgenerate_tokenで行う


                        else:
                            print("Error Operation Code")
                            self.sock.close()
            
        except Exception as e:
            self.sock.close()
            
    async def start(self):
        udp_task = asyncio.create_task(self.start_udp())
        tcp_task = asyncio.create_task(self.start_tcp())
        await asyncio.gather(udp_task,tcp_task)
                    





server_address = '0.0.0.0'
server_port = 9001
server_udp_port = 9000
sock = None
udp_sock = None
user_list = []

my_server = server(server_address,server_port,sock,udp_sock,user_list)
asyncio.run(my_server.start())
















                



