
# 🧠 Python Socket Programming: Multi-Client Chat Application

This is a terminal-based multi-client chat application built using **Python sockets and threading**. It allows multiple users to connect to a central server, chat in broadcast or private mode, and supports server-side commands for managing users.

---

## 🚀 Features

- ✅ Real-time multi-client communication using TCP
- ✅ Broadcast mode (public chat to all users)
- ✅ Private messaging using `/pm <user> <message>`
- ✅ Mode switching:
  - `/mode private` → switch to private mode
  - `/mode broadcast` → switch back to broadcast mode
- ✅ Client commands:
  - `/list` – show all online users
  - `/help` – show command help
- ✅ Server admin commands:
  - `/list` – view connected clients
  - `/kick <user>` – disconnect a user
  - `/shutdown` – shut down the server
  - `/help` – show admin command list
- ✅ Thread-safe handling for multiple connections
- ✅ Help messages shown automatically on connection

---

## 🛠️ Built With

- Python 3
- `socket` module (network communication)
- `threading` module (parallel handling of clients)

---

## 🧪 How to Run

### 1. Start the Server

```bash
python server.py
````

You’ll see logs in the terminal for each client that connects.

### 2. Start a Client (in a new terminal)

```bash
python client.py
```

Each client will be prompted to enter a nickname.

👉 You can run multiple clients in different terminals to test!

---

## 💬 Client Commands

| Command            | Description                         |
| ------------------ | ----------------------------------- |
| `/help`            | Show help menu                      |
| `/list`            | List all users currently online     |
| `/mode private`    | Switch to private messaging mode    |
| `/mode broadcast`  | Return to public broadcast chat     |
| `/pm <user> <msg>` | Send private message (one-time use) |

---

## 🔧 Server Admin Commands

| Command        | Description                           |
| -------------- | ------------------------------------- |
| `/list`        | Show all connected users              |
| `/kick <user>` | Forcefully disconnect a user          |
| `/shutdown`    | Close server and disconnect all users |
| `/help`        | Show admin help menu                  |

---

## 📸 Screenshots


---

## 📂 Folder Structure

```
Socket_programming/
├── client.py         # Client-side script
├── server.py         # Server-side script
└── README.md         # This file
```

---

## ✨ Future Ideas

* GUI client (Tkinter or PyQt)
* WebSocket-based version (for web clients)
* Encrypted messaging (SSL)
* Authentication/login system
* Chat logs or message history

---

## 🧑‍💻 Author

**@alamin72b** – Socket programming learner and builder
🔗 [GitHub Profile](https://github.com/alamin72b)

---

## 🪪 License

This project is open-source and free to use for learning and development purposes.

---

> Built with Python and curiosity 😊

````