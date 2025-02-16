#socketによる接続(server・client両方必要)
#データの受信
#json形式の読み込み
#id に対応したaddress のマップ作成
#各データ処理関数の実装
#処理データのjson形式への変換
#データクライアントへ送信

#イベント処理クラスprocess_event---
#   各リクエストに対応するインスタンス作成のためのクラス
#   メソッドには"method"に応じて処理できるexe_event(method,params)を実装し
#   resultを返す
import os
import json
import socket
import math

type_map = {
        "int":int,
        "float":float,
        "string":str,
        "bool":bool
}


class Function:
    #受け取ったデータの入力の型が，クライアント側で指定した型と一致しているか判定を行う関数
    @staticmethod
    def is_valid_type(param,param_types):
        #型2つ以上はリスト形式で来る([int,int])を想定
        #入力:param:クライアントのJSONを読み取ったデータ param_type:クライアントJSONのparam_types読み取ったデータ(文字列)
        print("tpye:params ",type(param))
        param=eval(param)
        param_types = eval(param_types)
        print("tpye:params ",type(param))
        if type(param) == list:
            #文字列になっているのでリストに変換
            param_list = param
            param_types = param_types
            
            print("param_list ",param_list)
            print("param_list ",param_types)


            i=0
            while i < len(param_list) :
                #指定された型と入力されたデータの型が同じか判定
                try:
                    print("type(param_list[i]) :",type(param_list[i]))
                    if type(param_list[i]) != param_types[i]:
                        print("list",type(param_list[i])," parat ",param_types[i])
                        return False
                except Exception as e:
                    print(e)
                    return False
                i+=1
            return True
            
        else:
            return type(param) == param_types
        

    @staticmethod
    def myfloor(params):
        return math.floor(params)

    @staticmethod
    def mynroot(params):
        n = params[0]
        x = params[1] #このデータの受け取り方に関するコードは要修正
        return math.log(x,n)

    @staticmethod
    def myreverse(params):
        temp_string = params[::-1]
        return temp_string
    
    @staticmethod
    def myvalidAnagram(params):
        #片方の文字列回して，一致すればその文字をもう片方から削除，それを繰り返して，一致しないか，回してる文字列が最後まで回ったらアナグラムであることを示す
        print("test")
        temp_string = params[1]
        for i in params[0]:  
            index = temp_string.find(i)
            if index == -1 and len(temp_string) >= 1:
                    return "False"
            print("temp_string:",temp_string)
            print("param[0]",i)
            temp_string = temp_string.replace(i,"",1)
        if len(temp_string) >= 1:
            return "False"
        return "True"        

    @staticmethod
    def mysort(params):
        sorted_string = sorted(params)
        return sorted_string
    


hash_map = {
        "floor": Function.myfloor,
        "nroot": Function.mynroot,
        "reverse": Function.myreverse,
        "validAnagram": Function.myvalidAnagram,
        "sort": Function.mysort   
}

#ソケットの作成やデータの送受信を管理するクラス
def determine_types(res_result):
                    if type(res_result) != list:
                        for k,v in type_map.items():
                            if type(res_result) == v:
                                type_list = k
                                return type_list
                        

                    else:
                        type_list = []
                        for ele in res_result:
                                for k,v in type_map.items():
                                    if type(ele) == v:
                                        type_list.append(k)
                        type_list = str(type_list)
                        return type_list          





class server:
    def __init__(self,socket_path,sock=None):
        self.socket_path = socket_path
        self.sock = sock
    def create_my_socket(self):
    #unix ドメインソケットの生成
        self.sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    def server_start(self):     
    #ソケット生成し，バインドやリッスンで接続待って，データが到着したら処理を開始する
        self.create_my_socket()
        self.sock.bind(self.socket_path)
        self.sock.listen(5)
       
        while True:
            connection,client_address = self.sock.accept()
            print("connection accecpted ",connection)
            data = connection.recv(1024)
            
            if data:

                #クライアントが送信してきたデータがJSON形式かどうか
                #try:
                #client_data = json.loads(data.decode('utf-8'))
                #except json.JSONDecodeError as e:
                
                client_data = json.loads(data.decode('utf-8'))
                print(client_data["method"] in hash_map)
                #指定されたメソッドがサーバ内に存在するか
                response_result = None
                
                if client_data["method"] in hash_map:


                    print("client_data['params']",client_data["params"],"  client_data['param_types']",client_data["param_types"])

                    #クライアント側の入力した引数と指定した引数の型があっているか
                    #具体的にはparamの型がparam_typesに準ずるか判定する
                    if Function.is_valid_type(client_data["params"],client_data["param_types"]):
                        response_result = hash_map[client_data["method"]](eval(client_data["params"]))                    
                    #型をそのままリストに載せるとJSONの変換時にエラーとなるから，文字にするためのmapの逆引きを行う
                    type_list = determine_types(response_result)

                    #リクエスト処理後のデータをJSONにするために，まずは辞書型で保持しておく
                    response_data = {
                            "results": response_result,
                            "result_type": type_list,
                            "id": client_data["id"]
                    }

                    connection.send(json.dumps(response_data).encode("utf-8"))
                    print("Sent!!")
#unix ドメインソケット用のファイルパス
def main():
    server_address = '/tmp/server_address'
    try:
        os.unlink('/tmp/server_address')
    except:
        pass
    my_server = server(server_address)
    my_server.server_start()

if __name__ == '__main__':
    main()
