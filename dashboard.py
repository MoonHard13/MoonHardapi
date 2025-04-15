import customtkinter as ctk
import threading
import json
import time
from dashboard_controller import DashboardController
from program_registry import PROGRAMS

SERVER_URL = "https://moonhardapi.onrender.com"
AUTH_TOKEN = "479a263f74007327498f24925a9ce0ae"
REFRESH_INTERVAL = 5  # seconds

class ClientDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Moonhard Client Monitor")
        self.geometry("700x700")
        self.controller = DashboardController(SERVER_URL, AUTH_TOKEN)

        # === Πίνακας πελατών ===
        self.clients_box = ctk.CTkTextbox(self, height=200, width=680)
        self.clients_box.pack(pady=10)

        # === Πίνακας αποτελεσμάτων ===
        self.status_box = ctk.CTkTextbox(self, height=150, width=680)
        self.status_box.pack(pady=10)

        # === Επιλογή προγραμμάτων ===
        self.checkbox_frame = ctk.CTkFrame(self)
        self.checkbox_frame.pack(pady=10)
        self.program_vars = {}
        for i, program in enumerate(PROGRAMS):
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(self.checkbox_frame, text=program, variable=var)
            chk.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="w")
            self.program_vars[program] = var

        # === Κουμπιά ===
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(pady=10)

        self.refresh_btn = ctk.CTkButton(self.buttons_frame, text="🔄 Refresh", command=self.refresh_status)
        self.refresh_btn.grid(row=0, column=0, padx=10)

        self.download_sel_btn = ctk.CTkButton(self.buttons_frame, text="⬇️ Download Selected", command=self.download_selected)
        self.download_sel_btn.grid(row=0, column=1, padx=10)

        self.download_all_btn = ctk.CTkButton(self.buttons_frame, text="📦 Download All", command=self.download_all)
        self.download_all_btn.grid(row=0, column=2, padx=10)
        self.install_sel_btn = ctk.CTkButton(self.buttons_frame, text="🛠️ Install Selected", command=self.install_selected)
        self.install_sel_btn.grid(row=1, column=1, padx=10, pady=(10,0))

        self.install_all_btn = ctk.CTkButton(self.buttons_frame, text="🧩 Install All", command=self.install_all)
        self.install_all_btn.grid(row=1, column=2, padx=10, pady=(10,0))
    

        self.refresh_status_loop()
    def install_selected(self):
        selected_programs = [name for name, var in self.program_vars.items() if var.get()]
        if not selected_programs:
            self.status_box.insert("end", "⚠️ No programs selected\n")
            return
        cmd = "install_selected:" + ",".join(selected_programs)
        result = self.controller.broadcast_command(cmd)
        self.status_box.insert("end", f"🛠️ {result}\n")

    def install_all(self):
        result = self.controller.broadcast_command("install_all")
        self.status_box.insert("end", f"🧩 {result}\n")

    def refresh_status(self):
        response = self.controller.get_status()
        self.clients_box.delete("1.0", "end")
        if isinstance(response, dict) and "error" in response:
            self.clients_box.insert("end", f"❌ Error: {response['error']}\n")
        else:
            for client in response:
                self.clients_box.insert("end", json.dumps(client, indent=2) + "\n")

    def download_selected(self):
        selected_programs = [name for name, var in self.program_vars.items() if var.get()]
        if not selected_programs:
            self.status_box.insert("end", "⚠️ No programs selected\n")
            return
        cmd = "download_selected:" + ",".join(selected_programs)
        result = self.controller.broadcast_command(cmd)
        self.status_box.insert("end", f"⬇️ {result}\n")

    def download_all(self):
        result = self.controller.broadcast_command("download_all")
        self.status_box.insert("end", f"📦 {result}\n")

    def refresh_status_loop(self):
        def loop():
            while True:
                self.refresh_status()
                time.sleep(REFRESH_INTERVAL)

        threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ClientDashboard()
    app.mainloop()
    