import asyncio
import websockets
import json
from datetime import datetime
from dotenv import load_dotenv
import random
import os

# Load environment variables (nếu cần)
load_dotenv()

# Device ID và URL của WebSocket server
DEVICE_ID = input("Enter device ID: ")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")
ENDPOINT = os.getenv("ENDPOINT")

async def send_log():
    async def send_ping(websocket):
        while True:
            try:
                await websocket.send("ping")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Ping failed: {e}")
                break

    async def connect_websocket():
        for attempt in range(5):
            try:
                websocket = await websockets.connect(f"{WEBSOCKET_URL}/logs/jetson-nano")
                print(f"Connected to server as {ENDPOINT}-{DEVICE_ID}")
                return websocket
            except Exception as e:
                print(f"Connection failed (attempt {attempt + 1}): {e}")
                await asyncio.sleep(5)
        return None

    websocket = await connect_websocket()
    if websocket is None:
        print("Failed to connect to server after multiple attempts.")
        return

    asyncio.create_task(send_ping(websocket))

    while True:
        try:
            log_data = {
                "username": random.choice(["maidung", "ngoctp"]),
                "device_id": DEVICE_ID,
                "name": random.choice(["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown"]),
                "photoUrl": "",
                "timestamp": int(datetime.now().timestamp()),
                "type": random.choice(["entry", "exit"]),
                "apartment": random.choice(["A-1203", "B-402", "C-305", "D-101"]),
            }
            
            await websocket.send(json.dumps(log_data))

            
            await asyncio.sleep(10)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection lost: {e}. Reconnecting...")
            websocket = await connect_websocket()
        except KeyboardInterrupt:
            print("Connection closed by user")
            if websocket:
                await websocket.close()
            break

asyncio.run(send_log())
