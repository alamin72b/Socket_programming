# client.py — Chat client that communicates with server using JSON

import socket
import threading
import json

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

nickname = input("Choose your nickname: ").strip()
client.send(nickname.encode('utf-8'))

# Track the current message mode
current_mode = "broadcast"
target_user = None

# Receive messages from server
def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("Disconnected from server.")
                break

            try:
                msg = json.loads(data.decode('utf-8'))
            except json.JSONDecodeError:
                print("Received invalid message from server.")
                continue

            msg_type = msg.get("type")

            # Handle public messages
            if msg_type == "message":
                print(f"\n{msg.get('from')}: {msg.get('content')}")

            # Handle private messages
            elif msg_type == "pm":
                print(f"\n[Private] {msg.get('from')} → {msg.get('to')}: {msg.get('content')}")

            # Server information (like welcome or shutdown)
            elif msg_type == "info":
                print(f"\n[INFO] {msg.get('content')}")

            # Server errors
            elif msg_type == "error":
                print(f"\n[ERROR] {msg.get('content')}")

        except:
            print("Error receiving message.")
            client.close()
            break

# Send messages to server
def send_messages():
    global current_mode, target_user
    while True:
        try:
            user_input = input()

            # Handle /mode command
            if user_input.startswith("/mode"):
                parts = user_input.split(" ", 1)
                if len(parts) < 2:
                    print("Usage: /mode [broadcast|private]")
                    continue
                mode = parts[1].strip().lower()
                if mode == "private":
                    # Ask for target user after listing others
                    client.send(json.dumps({
                        "type": "command",
                        "from": nickname,
                        "content": "list"
                    }).encode('utf-8'))
                    print("(Wait a second to see the list)")
                    target_user = input("Enter username to send private messages to: ").strip()
                    current_mode = "private"
                    print(f"Private mode ON. Messages go to '{target_user}'.")
                elif mode == "broadcast":
                    current_mode = "broadcast"
                    target_user = None
                    print("Broadcast mode ON.")
                else:
                    print("Unknown mode. Use /mode [broadcast|private]")
                continue

            # Handle other slash commands
            elif user_input.startswith("/list") or user_input.startswith("/help"):
                msg_obj = {
                    "type": "command",
                    "from": nickname,
                    "content": user_input.lstrip("/")
                }
                client.send(json.dumps(msg_obj).encode('utf-8'))
                continue

            # Send public or private message
            if current_mode == "broadcast":
                msg_obj = {
                    "type": "message",
                    "from": nickname,
                    "content": user_input
                }
            elif current_mode == "private":
                if target_user:
                    msg_obj = {
                        "type": "pm",
                        "from": nickname,
                        "to": target_user,
                        "content": user_input
                    }
                else:
                    print("No target set. Use /mode private to choose a user.")
                    continue

            client.send(json.dumps(msg_obj).encode('utf-8'))

        except:
            print("Error sending message.")
            client.close()
            break

# Start threads
threading.Thread(target=receive_messages, daemon=True).start()
send_messages()
