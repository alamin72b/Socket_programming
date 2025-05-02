import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5557))
server.listen()

print("Server is listening on localhost:5555...")

clients = []
nicknames = []
client_map = {}  # nickname -> client socket
lock = threading.Lock()

def broadcast(message, sender_client=None):
    with lock:
        for client in clients:
            if client != sender_client:
                try:
                    client.send(message)
                except:
                    remove_client(client)

def remove_client(client):
    with lock:
        if client in clients:
            index = clients.index(client)
            nickname = nicknames.pop(index)
            clients.remove(client)
            client_map.pop(nickname, None)
            client.close()
            broadcast(f"{nickname} has left the chat.".encode('utf-8'), client)
            print(f"{nickname} disconnected.")

def handle_client(client):
    try:
        help_message = (
            "Welcome to the chat!\n"
            "Commands:\n"
            " - Type normally to chat publicly\n"
            " - /mode private     → Switch to private mode\n"
            " - /mode broadcast   → Switch to broadcast mode\n"
            " - /pm <user> <msg>  → Send a private message\n"
            " - /list             → Show online users\n"
            " - /help             → Show this menu again\n"
        )
        client.send(help_message.encode('utf-8'))

        while True:
            message = client.recv(1024)
            if not message:
                break
            decoded = message.decode('utf-8').strip()

            sender_index = clients.index(client)
            sender_name = nicknames[sender_index]

            if decoded == "/help":
                client.send(help_message.encode('utf-8'))

            elif decoded == "/list":
                with lock:
                    others = [n for n in nicknames if n != sender_name]
                    online = ", ".join(others) if others else "(no one else online)"
                client.send(f"Online users: {online}".encode('utf-8'))

            elif decoded.startswith("/pm "):
                try:
                    parts = decoded.split(" ", 2)
                    if len(parts) < 3:
                        raise ValueError
                    target_name = parts[1]
                    private_message = parts[2]

                    with lock:
                        if target_name in client_map:
                            full_msg = f"[Private] {sender_name}: {private_message}".encode('utf-8')
                            client_map[target_name].send(full_msg)
                        else:
                            client.send(f"User '{target_name}' not found. Type /list to see who is online.".encode('utf-8'))
                except:
                    client.send("Invalid format. Use: /pm <user> <message>".encode('utf-8'))

            else:
                broadcast(f"{sender_name}: {decoded}".encode('utf-8'), client)

    except:
        pass
    remove_client(client)

def show_server_help():
    print("\n[Server Commands]")
    print(" /list       - Show connected client nicknames")
    print(" /kick NAME  - Kick user by nickname")
    print(" /shutdown   - Close server and disconnect all clients")
    print(" /help       - Show this help menu")
    print(" (Type any message to broadcast to all clients)\n")

def server_input():
    while True:
        command = input()
        if command == "/list":
            with lock:
                print("Connected clients:", nicknames)
        elif command.startswith("/kick "):
            name = command.split(" ", 1)[1]
            with lock:
                if name in client_map:
                    client = client_map[name]
                    client.send("You have been kicked.".encode('utf-8'))
                    remove_client(client)
                    print(f"Kicked {name}")
                else:
                    print(f"No client with nickname '{name}' found.")
        elif command == "/shutdown":
            print("Shutting down server...")
            with lock:
                for client in clients:
                    try:
                        client.send("Server is shutting down.".encode('utf-8'))
                        client.close()
                    except:
                        pass
                clients.clear()
                nicknames.clear()
                client_map.clear()
            server.close()
            break
        elif command == "/help":
            show_server_help()
        else:
            broadcast(f"SERVER: {command}".encode('utf-8'), None)

def receive():
    while True:
        try:
            client, _ = server.accept()
            nickname = client.recv(1024).decode('utf-8').strip()

            with lock:
                if nickname in nicknames:
                    client.send("Nickname already taken.".encode('utf-8'))
                    client.close()
                    continue
                nicknames.append(nickname)
                clients.append(client)
                client_map[nickname] = client

            print(f"{nickname} connected.")
            broadcast(f"{nickname} joined the chat.".encode('utf-8'), client)
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
        except:
            break

# Show help when server starts
show_server_help()

threading.Thread(target=server_input, daemon=True).start()
receive()
