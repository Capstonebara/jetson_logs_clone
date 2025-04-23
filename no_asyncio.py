import json
from datetime import datetime
import random
import os
import time
import threading
import websocket  # pip install websocket-client

# Device ID and WebSocket server URL
DEVICE_ID = input("Enter device ID: ")
ENDPOINT = "123"

def send_ping(ws):
    while True:
        try:
            ws.send("ping")
            time.sleep(5)
        except Exception as e:
            print(f"Ping failed: {e}")
            break

def connect_websocket():
    for attempt in range(5):
        try:
            ws = websocket.create_connection(f"wss://api.fptuaiclub.me/logs/{DEVICE_ID}")
            print(f"Connected to server as {ENDPOINT}-{DEVICE_ID}")
            return ws
        except Exception as e:
            print(f"Connection failed (attempt {attempt + 1}): {e}")
            time.sleep(5)
    return None

def send_image(ws, image_path):
    """
    Sends an image file as binary data over the WebSocket connection.
    """
    try:
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()
        
        ws.send("image")
        ws.send_binary(image_data)
        print(f"Image sent: {image_path}")
    except FileNotFoundError:
        print(f"Image file not found: {image_path}")
    except Exception as e:
        print(f"Failed to send image: {e}")

def send_log():
    ws = connect_websocket()
    if ws is None:
        print("Failed to connect to server after multiple attempts.")
        return

    # Start ping thread
    ping_thread = threading.Thread(target=send_ping, args=(ws,), daemon=True)
    ping_thread.start()

    try:
        while True:
            try:
                log_data = {
                    "username": random.choice(["maidung", "ngoctp"]),
                    "device_id": DEVICE_ID,
                    "name": random.choice(["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown"]),
                    "timestamp": int(datetime.now().timestamp()),
                    "type": random.choice(["entry", "exit"]),
                    "apartment": random.choice(["A-1203", "B-402", "C-305", "D-101"]),
                }
                
                ws.send(json.dumps(log_data))
                print("Log sent:", log_data)

                image_path = f"./data/{random.randint(1, 2)}.jpg"
                send_image(ws, image_path)

                time.sleep(10)

            except websocket.WebSocketConnectionClosedException as e:
                print(f"Connection lost: {e}. Reconnecting...")
                ws = connect_websocket()
                if ws:
                    ping_thread = threading.Thread(target=send_ping, args=(ws,), daemon=True)
                    ping_thread.start()
                
    except KeyboardInterrupt:
        print("Connection closed by user")
        if ws:
            ws.close()

# Run the WebSocket client
if __name__ == "__main__":
    send_log()
