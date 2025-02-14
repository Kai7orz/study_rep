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


def myfloor(params):
    return math.floor(params)


def mynroot(params):
    n = params[0]
    x = params[1] #このデータの受け取り方に関するコードは要修正
    return math.log(x,n)

def myreverse(params):
    temp_string = params[::-1]
    return temp_string
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

def mysort(params):
    sorted_string = sorted(params)
    return sorted_string
    



class process_event:
    
    def __init__(self,method,params,param_types,id,result,result_type):
        self.method = method
        self.params = params
        self.param_types = param_types
        self.id = id
        self.result = result
        self.result_type = result_type


    def exe_event(self):
        if self.method == "floor":
            self.result = myfloor(self.params)
            self.result_type = "int"

        elif self.method == "nroot":
            self.result = mynroot(self.params)
            self.result_type = "float"

        elif self.method == "reverse":
            self.result = myreverse(self.params)
            self.result_type = "string"

        elif self.method == "validAnagram":
            self.result = myvalidAnagram(self.params)
            self.result_type = "bool"

        elif self.method == "sort":
            self.result = mysort(self.params)
            self.result_type = self.param_types

server_address = ('localhost',8000)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.bind(server_address)
sock.listen(1)

while True:
    connection,client_address = sock.accept()

    data = connection.recv(4096)
    print("this is ",data)
    if data:
        my_data = json.loads(data.decode('utf-8'))
        print(my_data)
        
        req = process_event(my_data["method"],my_data["params"],my_data["param_types"],my_data["id"],result=None,result_type=None)
        req.exe_event()
        response_data = {
            "results": req.result,
            "result_type": req.result_type,
            "id": req.id
        }

        response_data = json.dumps(response_data,ensure_ascii=False,indent=2)
        sent = connection.send(response_data.encode('utf-8'))
