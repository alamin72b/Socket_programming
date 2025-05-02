# Socket_programming
# 🧠 Python Socket Programming: Multi-Client Chat Application

This is a terminal-based multi-client chat application built using **Python sockets and threading**. It allows multiple users to connect to a server, send broadcast or private messages, and use server-side/admin commands.

---

## 🚀 Features

- ✅ Real-time multi-client chat over TCP
- ✅ Broadcast mode (chat with everyone)
- ✅ Private mode with `/pm <user> <message>`
- ✅ Command support:
  - `/list` – view online users
  - `/help` – show help menu
  - `/mode private` – switch to private mode
  - `/mode broadcast` – switch to broadcast mode
- ✅ Server admin commands:
  - `/list`, `/kick <user>`, `/shutdown`, `/help`
- ✅ Thread-safe communication handling

---

## 🛠️ Technologies Used

- Python 3
- `socket` module
- `threading` module

---

## 🧪 How to Run

### 🔹 Step 1: Start the Server

```bash
python server.py

🔹 Step 2: Start a Client (in a separate terminal)

python client.py

👉 You can run as many clients as you want, in different terminals.
📸 Screenshots

(Optional: Add terminal screenshots showing broadcasting, private chat, list command, etc.)
📚 Example Commands
On the Client:

    /list → See who is online

    /mode private → Switch to private chat (then enter username)

    /mode broadcast → Return to public chat

    /pm <user> <message> → Send one-time private message

    /help → Show command guide

On the Server Console:

    /list → Show all connected nicknames

    /kick <nickname> → Disconnect a user

    /shutdown → Shut down the server and all clients

    /help → Show admin command menu

🤝 Contributing

Pull requests are welcome! If you find bugs or want to add features (like chat logs, UI, or authentication), feel free to contribute.
🪪 License

This project is open-source. Feel free to use it for learning or improve upon it.
✨ Acknowledgment

Built as a hands-on learning project while exploring Python’s socket programming.