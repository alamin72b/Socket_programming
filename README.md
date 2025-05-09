
# 🧠 Python Socket Programming: JSON-Based Multi-Client Chat Application

This is a terminal-based multi-client chat application built using **Python sockets**, **threading**, and a structured **JSON message protocol**. It supports real-time messaging between clients connected to a central server. Messages are sent and received in a structured JSON format for better extensibility and maintainability.

---

## 🚀 Features

- ✅ Real-time multi-client chat over TCP
- ✅ Structured JSON protocol for all messages
- ✅ Broadcast mode for public chat
- ✅ Private messaging via `/mode private`
- ✅ Mode switching:
  - `/mode private` → enable private chat mode
  - `/mode broadcast` → switch back to public mode
- ✅ Client-side commands:
  - `/list` – show currently online users
  - `/help` – show command help
- ✅ Server-side commands:
  - `/list` – view connected users
  - `/kick <user>` – disconnect a user
  - `/shutdown` – stop server and disconnect all clients
  - `/help` – display admin help
- ✅ Thread-safe server using `threading.Lock`
- ✅ Informative feedback and error handling using JSON messages
- ✅ Clear beginner-friendly code comments for learning purposes

---

## 🛠️ Built With

- Python 3
- `socket` – for TCP networking
- `threading` – for concurrent client handling
- `json` – for structured message exchange

---

## 📦 JSON Message Format

All messages exchanged between client and server follow a consistent JSON format:

```json
{
  "type": "message" | "pm" | "command" | "info" | "error",
  "from": "Alice",
  "to": "Bob",
  "content": "Hello!"
}
````

| Field     | Description                             |
| --------- | --------------------------------------- |
| `type`    | Type of message (`message`, `pm`, etc.) |
| `from`    | Sender's nickname                       |
| `to`      | Receiver's nickname (for private only)  |
| `content` | Actual message text or command          |

---

## 🧪 How to Run

### 1. Start the Server

```bash
python server.py
```

> This will start the server and wait for client connections.

### 2. Start a Client (in a new terminal window)

```bash
python client.py
```

> Enter a nickname when prompted. You can open multiple clients in different terminals to simulate a chatroom.

---

## 💬 Client Commands

| Command            | Description                      |
| ------------------ | -------------------------------- |
| `/help`            | Show available commands          |
| `/list`            | List online users                |
| `/mode private`    | Switch to private messaging mode |
| `/mode broadcast`  | Return to public chat mode       |
| `/pm <user> <msg>` | One-time private message         |

---

## 🔧 Server Admin Commands

| Command        | Description                     |
| -------------- | ------------------------------- |
| `/list`        | View all connected nicknames    |
| `/kick <user>` | Disconnect a user by nickname   |
| `/shutdown`    | Gracefully shut down the server |
| `/help`        | Show server command help        |

---

## 📂 Folder Structure

```
Socket_programming/
├── client.py         # Terminal-based chat client
├── server.py         # Central chat server
└── README.md         # Project documentation
```

---

## ✨ Future Enhancements

* GUI client (Tkinter or PyQt)
* WebSocket support for browser-based chat
* SSL/TLS encryption for secure messaging
* User authentication and login system
* Chat log storage (file or database)

---

## 👤 Author

**@alamin72b**
Socket programming learner and builder
🔗 [GitHub Profile](https://github.com/alamin72b)

---

## 🪪 License

This project is open-source and free to use for educational or development purposes.

> Built with Python, curiosity, and a JSON mindset 😊

