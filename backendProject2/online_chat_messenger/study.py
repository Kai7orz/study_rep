import time
import asyncio

#入力して間に10秒後のメッセージ受信機能作成す
async def sendMessage():
    message = await asyncio.to_thread(input, "入力してください: ")
    print(message)
    await asyncio.sleep(2) #send
    return message


async def recvMessage():
    await asyncio.sleep(4)
    print("message received")
    return "test"

async def main():
    while True:
        result = await asyncio.gather(sendMessage(),recvMessage())
    
asyncio.run(main())