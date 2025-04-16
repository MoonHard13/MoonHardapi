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
        self.title("🖥️ Moonhard Client Dashboard")
        self.geometry("1000x600")
        self.minsize(900, 500)
        self.controller = DashboardController(SERVER_URL, AUTH_TOKEN)
        self.selected_client = None

        self.grid_columnconfigure(0, weight=1, uniform="col")
        self.grid_columnconfigure(1, weight=2, uniform="col")
        self.grid_rowconfigure(0, weight=1)

        # === Client List Panel ===
        self.client_panel = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.client_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        self.client_label = ctk.CTkLabel(self.client_panel, text="🖥️ Connected Clients", font=("Segoe UI", 16, "bold"))
        self.client_label.pack(pady=(10, 5))

        self.clients_scroll = ctk.CTkScrollableFrame(self.client_panel, width=280, height=550)
        self.clients_scroll.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.client_buttons = {}

        # === Control Panel ===
        self.control_panel = ctk.CTkFrame(self, corner_radius=10)
        self.control_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        self.checkbox_frame = ctk.CTkFrame(self.control_panel)
        self.checkbox_frame.pack(pady=(10, 5), padx=10, fill="x")

        self.program_vars = {}
        for i, program in enumerate(PROGRAMS):
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(self.checkbox_frame, text=program, variable=var)
            chk.grid(row=i//3, column=i%3, padx=5, pady=3, sticky="w")
            self.program_vars[program] = var

        self.buttons_frame = ctk.CTkFrame(self.control_panel)
        self.buttons_frame.pack(pady=10, padx=10)

        self.refresh_btn = ctk.CTkButton(self.buttons_frame, text="🔄 Refresh", command=self.refresh_status, width=140)
        self.refresh_btn.grid(row=0, column=0, padx=5, pady=5)

        self.download_sel_btn = ctk.CTkButton(self.buttons_frame, text="⬇️ Download Selected", command=self.download_selected, width=180)
        self.download_sel_btn.grid(row=0, column=1, padx=5, pady=5)

        self.download_all_btn = ctk.CTkButton(self.buttons_frame, text="📦 Download All", command=self.download_all, width=140)
        self.download_all_btn.grid(row=0, column=2, padx=5, pady=5)

        self.install_sel_btn = ctk.CTkButton(self.buttons_frame, text="🛠️ Install Selected", command=self.install_selected, width=180)
        self.install_sel_btn.grid(row=1, column=1, padx=5, pady=5)

        self.install_all_btn = ctk.CTkButton(self.buttons_frame, text="🧩 Install All", command=self.install_all, width=140)
        self.install_all_btn.grid(row=1, column=2, padx=5, pady=5)

        self.status_box = ctk.CTkTextbox(self.control_panel, height=180)
        self.status_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.refresh_status_loop()

    def select_client(self, client_id):
        self.selected_client = client_id
        self.status_box.insert("end", f"🟢 Selected client: {client_id}\n")

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
        for widget in self.clients_scroll.winfo_children():
            widget.destroy()

        if isinstance(response, dict) and "error" in response:
            self.status_box.insert("end", f"❌ Error: {response['error']}\n")
        else:
            for client in response:
                client_id = client.get("client_id", "Unknown")
                btn = ctk.CTkButton(self.clients_scroll, text=client_id, width=260,
                                    command=lambda cid=client_id: self.select_client(cid))
                btn.pack(pady=2)
                self.client_buttons[client_id] = btn

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
            self.refresh_status()
            self.after(REFRESH_INTERVAL * 1000, loop)
        self.after(0, loop)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ClientDashboard()
    app.mainloop()