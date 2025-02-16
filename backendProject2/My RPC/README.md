# remote-procedure-call

## 概要
node.js 側のクライアントが入力したデータを，Pythonで記述されたサーバが処理を行うJSON-RPCです.

## 実行方法
サーバー側
```
python3 rpc-server.py
```
クライアント側
```
node rpc-client.js
```

### クライアント側

#### method
method: 実行したいメソッド名を指定(floor,nroot,reverse,validAnagram,sort)

##### param
各metod に対する引数を指定
floor: float
nroot: int,int
reverse: str
validAnagram: str,str
sort: str,str,...

##### param_types
floor: float
nroot: [int,int]
reverse: str
validAnagram: [str,str]
sort: [str,str,...]

## 実際の動作(写真)

![image](./img/result_floor.png)
![image](./img/result_nroot.png)
![image](./img/result_reverse.png)
![image](./img/result_validAnagram.png)
![image](./img/result_sort.png)
