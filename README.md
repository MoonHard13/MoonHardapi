
# 🌙 MoonHard Remote Management System

> A complete real-time client control and update system built with FastAPI, WebSockets, and CustomTkinter GUI. Designed for managing multiple client PCs remotely with installer control, real-time system monitoring, scheduled tasks, and more.

---

## 📦 Features

### ✅ Client Management
- Register/detect clients by unique ID
- Rename clients via GUI
- View live status (CPU, RAM, Disk)

### 🧠 System Monitoring
- Real-time CPU, RAM, Disk usage
- Uptime tracking
- IP, MAC, and OS information (upcoming)

### 📁 Remote Installers
- Installer execution for:
  - Amvrosia Service
  - SnService
  - CallServer Host/Client
  - External APIs
  - Main ERP Apps
- Download & unzip from Google Drive folders using PyDrive2
- Pattern-based cleanup before install

### 🛠️ Scheduled Tasks
- Schedule commands to run on clients (e.g., restart, install, clean temp)
- Persistent via JSON
- Supports repeatable tasks

### 📊 Dashboard GUI (CustomTkinter)
- Multi-client view
- Status indicators
- Installer actions
- Scheduled task manager (coming soon)
- Live logs & SQL backup triggering

### 🔁 Remote SQL Backup
- Reads SQL connection string from `appsettings.production.json`
- Performs `.bak` SQL backup to predefined location
- Supports zipped backup handling

### 📤 Telegram/Discord Integration (optional)
- Send remote commands via bot (e.g., `/install_all`, `/status`)

---

## 🧱 Architecture

```
📁 moonhard/
│
├── server/
│   ├── main.py              # FastAPI WebSocket server
│   ├── endpoints.py         # /register, /send, /broadcast
│   ├── clients.json         # Registered clients
│   └── logger.py            # Command log writer
│
├── client/
│   ├── agent.py             # Tray app + WebSocket client
│   ├── installers/          # Modular installer classes
│   ├── downloader.py        # GDrive zip download/extract
│   └── system_info.py       # CPU, RAM, Disk fetcher
│
├── dashboard/
│   ├── gui.py               # Main CustomTkinter dashboard
│   ├── widgets/             # Reusable UI widgets
│   ├── styles/              # Theme, icons, logos
│   └── logic/               # Button callbacks, events
│
└── shared/
    ├── config.py            # Paths, tokens, settings
    └── utils.py             # Common helpers
```

---

## 🚀 Setup Guide

### 🖥 Server

```bash
cd moonhard/server
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 🖥 Client (Tray App)

```bash
cd moonhard/client
pip install -r requirements.txt
python agent.py
```

This will auto-register the client, connect to the server, and wait for commands.

### 🖥 Dashboard (GUI Control Panel)

```bash
cd moonhard/dashboard
pip install -r requirements.txt
python gui.py
```

---

## 📂 Google Drive Setup

All installers are downloaded from predefined Drive folders. Set your credentials once via browser authentication on first run.

Required:
- `mycreds.txt` will be stored in `C:\SunsoftSetups\MoonHardRemote`

---

## 🔐 Credentials & Tokens

Update `shared/config.py` with your:
- WebSocket token
- Default download directory
- Admin credentials (if login is enabled)

---

## 📓 Roadmap

- [ ] Task Editor UI
- [ ] Live Graphs (CPU/RAM/Disk)
- [ ] Login System with roles
- [ ] Remote File Browser
- [ ] Multi-language support
- [ ] Mobile app dashboard

---

## 🧑‍💻 Contributors

- **Main Developer**: [@MoonHard13](https://github.com/MoonHard13)
- Special thanks to the CustomTkinter & FastAPI communities ❤️

---

## 🪪 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🛰 Screenshots

> Coming soon — preview the dashboard and client tray UI.

---
