import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5557))

nickname = input("Choose your nickname: ").strip()
client.send(nickname.encode('utf-8'))

current_mode = "broadcast"
target_user = None

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print("\n" + message)
            else:
                print("Disconnected from server.")
                client.close()
                break
        except:
            print("Error receiving message.")
            client.close()
            break

def send_messages():
    global current_mode, target_user
    while True:
        try:
            user_input = input()

            if user_input.startswith("/mode"):
                parts = user_input.split(" ", 1)
                if len(parts) < 2:
                    print("Usage: /mode [broadcast|private]")
                    continue
                mode = parts[1].strip().lower()
                if mode == "private":
                    client.send("/list".encode('utf-8'))
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

            elif user_input.startswith("/list") or user_input.startswith("/help") or user_input.startswith("/pm "):
                client.send(user_input.encode('utf-8'))
                continue

            if current_mode == "broadcast":
                message = user_input
                client.send(message.encode('utf-8'))
            elif current_mode == "private":
                if target_user:
                    pm_command = f"/pm {target_user} {user_input}"
                    client.send(pm_command.encode('utf-8'))
                else:
                    print("No target set. Use /mode private to choose a user.")
        except:
            print("Error sending message.")
            client.close()
            break

threading.Thread(target=receive_messages, daemon=True).start()
send_messages()
