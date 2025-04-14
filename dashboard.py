import customtkinter as ctk
import requests
import threading
import json

SERVER_URL = "https://moonhardapi.onrender.com"
AUTH_TOKEN = "479a263f74007327498f24925a9ce0ae"
REFRESH_INTERVAL = 5  # seconds

class ClientDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Moonhard Client Monitor")
        self.geometry("700x500")

        # === Πίνακας πελατών ===
        self.clients_box = ctk.CTkTextbox(self, height=250, width=680)
        self.clients_box.pack(pady=10)

        # === Πίνακας αποτελεσμάτων ===
        self.status_box = ctk.CTkTextbox(self, height=150, width=680)
        self.status_box.pack(pady=10)

        # === Κουμπιά ===
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(pady=10)

        self.refresh_btn = ctk.CTkButton(self.buttons_frame, text="🔄 Refresh", command=self.refresh_status)
        self.refresh_btn.grid(row=0, column=0, padx=10)


        self.broadcast_btn = ctk.CTkButton(self.buttons_frame, text="📡 Broadcast get_status", command=self.broadcast_status)
        self.broadcast_btn.grid(row=0, column=2, padx=10)


        self.refresh_status_loop()

    def refresh_status(self):
        try:
            response = requests.get(f"{SERVER_URL}/status")
            clients = response.json()
            self.clients_box.delete("1.0", "end")
            for client in clients:
                self.clients_box.insert("end", json.dumps(client, indent=2) + "\n")
        except Exception as e:
            self.clients_box.insert("end", f"❌ Error fetching status: {e}\n")

    def broadcast_status(self):
        try:
            response = requests.post(
                f"{SERVER_URL}/broadcast?token={AUTH_TOKEN}",
                json={"command": "get_status"}
            )
            self.status_box.insert("end", f"📡 Broadcast: {response.json()}\n")
        except Exception as e:
            self.status_box.insert("end", f"❌ Broadcast error: {e}\n")

    def refresh_status_loop(self):
        def loop():
            while True:
                self.refresh_status()
                time.sleep(REFRESH_INTERVAL)

        import time
        threading.Thread(target=loop, daemon=True).start()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ClientDashboard()
    app.mainloop()
