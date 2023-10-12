# client.py
import asyncio
import websockets


async def chat_with_bot():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            user_input = input("Client: ")
            await websocket.send(user_input)
            response = await websocket.recv()
            print(response)

asyncio.get_event_loop().run_until_complete(chat_with_bot())
