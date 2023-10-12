import asyncio
import websockets


async def chatbot_logic(websocket, path):
    async for message in websocket:
        response = f"Chatbot: You said '{message}'"
        await websocket.send(response)

start_server = websockets.serve(chatbot_logic, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
