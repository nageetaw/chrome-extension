import asyncio, websockets, json

connected = set()

async def handler(websocket):
    connected.add(websocket)
    try:
        async for msg in websocket:
            data = json.loads(msg)
            print("Received:", data)
    finally:
        connected.remove(websocket)

async def send_command(cmd):
    for ws in connected:
        await ws.send(json.dumps(cmd))

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Bridge running on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
