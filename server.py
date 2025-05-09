# server.py — Multi-client chat server using JSON protocol

import socket
import threading
import json

# Create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))  # Bind to localhost on port 5555
server.listen()

print("Server is listening on localhost:5555...")

# Lists to track connected clients and nicknames
clients = []
nicknames = []
client_map = {}  # Maps nickname to socket
lock = threading.Lock()  # For thread-safe operations

# Send a message to all clients except the sender
def broadcast(message_dict, sender_client=None):
    message_json = json.dumps(message_dict).encode('utf-8')
    with lock:
        for client in clients:
            if client != sender_client:
                try:
                    client.send(message_json)
                except:
                    remove_client(client)

# Remove a client from all lists and notify others
def remove_client(client):
    with lock:
        if client in clients:
            index = clients.index(client)
            nickname = nicknames.pop(index)
            clients.remove(client)
            client_map.pop(nickname, None)
            client.close()
            # Notify others that the user has left
            broadcast({"type": "info", "content": f"{nickname} has left the chat."}, client)
            print(f"{nickname} disconnected.")

# Handle messages from a single client
def handle_client(client):
    try:
        help_message = (
            "Welcome to the chat!\n"
            "Commands:\n"
            " - /mode private     → Switch to private mode\n"
            " - /mode broadcast   → Switch to broadcast mode\n"
            " - /pm <user> <msg>  → Send a private message\n"
            " - /list             → Show online users\n"
            " - /help             → Show this menu again\n"
        )
        # Send initial welcome/help message
        client.send(json.dumps({"type": "info", "content": help_message}).encode('utf-8'))

        while True:
            data = client.recv(1024)
            if not data:
                break

            # Decode and parse the incoming JSON message
            try:
                msg = json.loads(data.decode('utf-8'))
            except json.JSONDecodeError:
                client.send(json.dumps({"type": "error", "content": "Invalid message format."}).encode('utf-8'))
                continue

            msg_type = msg.get("type")
            sender_name = msg.get("from")
            content = msg.get("content")

            # Handle public message
            if msg_type == "message":
                broadcast({"type": "message", "from": sender_name, "content": content}, client)

            # Handle private message
            elif msg_type == "pm":
                target = msg.get("to")
                with lock:
                    if target in client_map:
                        private_msg = {
                            "type": "pm",
                            "from": sender_name,
                            "to": target,
                            "content": content
                        }
                        client_map[target].send(json.dumps(private_msg).encode('utf-8'))
                    else:
                        client.send(json.dumps({
                            "type": "error",
                            "content": f"User '{target}' not found. Use /list to see online users."
                        }).encode('utf-8'))

            # Handle commands like /help and /list
            elif msg_type == "command":
                if content == "help":
                    client.send(json.dumps({"type": "info", "content": help_message}).encode('utf-8'))
                elif content == "list":
                    with lock:
                        others = [n for n in nicknames if n != sender_name]
                        online = ", ".join(others) if others else "(no one else online)"
                    client.send(json.dumps({"type": "info", "content": f"Online users: {online}"}).encode('utf-8'))

    except:
        pass

    remove_client(client)

# Shows command options on the server terminal
def show_server_help():
    print("\n[Server Commands]")
    print(" /list       - Show connected client nicknames")
    print(" /kick NAME  - Kick user by nickname")
    print(" /shutdown   - Close server and disconnect all clients")
    print(" /help       - Show this help menu")
    print(" (Type any message to broadcast to all clients)\n")

# Allows server admin to type commands
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
                    client.send(json.dumps({"type": "info", "content": "You have been kicked."}).encode('utf-8'))
                    remove_client(client)
                    print(f"Kicked {name}")
                else:
                    print(f"No client with nickname '{name}' found.")
        elif command == "/shutdown":
            print("Shutting down server...")
            with lock:
                for client in clients:
                    try:
                        client.send(json.dumps({"type": "info", "content": "Server is shutting down."}).encode('utf-8'))
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
            # Broadcast admin message
            broadcast({"type": "info", "content": f"SERVER: {command}"}, None)

# Accept new client connections
def receive():
    while True:
        try:
            client, _ = server.accept()
            nickname = client.recv(1024).decode('utf-8').strip()

            with lock:
                if nickname in nicknames:
                    client.send(json.dumps({"type": "error", "content": "Nickname already taken."}).encode('utf-8'))
                    client.close()
                    continue
                nicknames.append(nickname)
                clients.append(client)
                client_map[nickname] = client

            print(f"{nickname} connected.")
            broadcast({"type": "info", "content": f"{nickname} joined the chat."}, client)
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
        except:
            break

# Start the server
show_server_help()
threading.Thread(target=server_input, daemon=True).start()
receive()
