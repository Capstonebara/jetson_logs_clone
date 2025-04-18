import asyncio
import websockets
import json
from datetime import datetime
from dotenv import load_dotenv
import random
import os

# Load environment variables (if needed)
load_dotenv()

# Device ID and WebSocket server URL
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
                websocket = await websockets.connect(f"wss://api.fptuaiclub.me/logs/{DEVICE_ID}")
                print(f"Connected to server as {ENDPOINT}-{DEVICE_ID}")
                return websocket
            except Exception as e:
                print(f"Connection failed (attempt {attempt + 1}): {e}")
                await asyncio.sleep(5)
        return None

    async def send_image(websocket, image_path):
        """
        Sends an image file as binary data over the WebSocket connection.
        """
        try:
            # Open the image file in binary mode
            with open(image_path, "rb") as img_file:
                image_data = img_file.read()
            
            # Send a message indicating that binary data is being sent
            await websocket.send("image")
            
            # Send the binary image data
            await websocket.send(image_data)
            print(f"Image sent: {image_path}")
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception as e:
            print(f"Failed to send image: {e}")

    websocket = await connect_websocket()
    if websocket is None:
        print("Failed to connect to server after multiple attempts.")
        return

    asyncio.create_task(send_ping(websocket))

    while True:
        try:
            # Send log data as JSON text
            log_data = {
                "username": random.choice(["maidung", "ngoctp"]),
                "device_id": DEVICE_ID,
                "name": random.choice(["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown"]),
                "timestamp": int(datetime.now().timestamp()),
                "type": random.choice(["entry", "exit"]),
                "apartment": random.choice(["A-1203", "B-402", "C-305", "D-101"]),
            }
            
            await websocket.send(json.dumps(log_data))
            print("Log sent:", log_data)

            # Send an image after sending the log (optional)
            image_path = f"./data/{random.randint(1, 2)}.jpg"  # Random image 1 or 2
            await send_image(websocket, image_path)

            # Wait before sending the next log and image
            await asyncio.sleep(10)

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection lost: {e}. Reconnecting...")
            websocket = await connect_websocket()
        except KeyboardInterrupt:
            print("Connection closed by user")
            if websocket:
                await websocket.close()
            break

# Run the WebSocket client
asyncio.run(send_log())