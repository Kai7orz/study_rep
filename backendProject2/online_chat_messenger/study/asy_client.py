import asyncio 

clients = []

async def handle_client(reader,writer):
    clients.append(writer)

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode('utf-8')
            for client in clients:
                client.write(data)
            await asyncio.gather(*(client.drain() for client in clients))
    finally:
        clients.remove(writer)
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client,'127.0.0.1',8888)
    await server.serve_forever()

asyncio.run(main())