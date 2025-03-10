class user:
    def __init__(self,user_name,transmit_time,message):
        self.user_name = user_name 
        self.transmit = transmit_time
        self.message = message
        self.udp_socket = None

    def start_session(self):
        #udpソケットの生成とサーバip,port入力
        server_ip = input("server address ?")
        server_port = input("server port?")

        server_address = (server_ip,server_port)
        