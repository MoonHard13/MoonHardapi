import customtkinter as ctk
import threading
import json 
import time
from dashboard_controller import DashboardController
from program_registry import PROGRAMS
import datetime
from tkinter import messagebox

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
        self.last_messages_seen = {}
        self.selected_client = None
        self.client_names = self.load_client_names()

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

        self.backup_btn = ctk.CTkButton(self.buttons_frame, text="💾 Backup", command=self.backup_command, width=140)
        self.backup_btn.grid(row=1, column=0, padx=5, pady=5)

        self.status_box = ctk.CTkTextbox(self.control_panel, height=180)
        self.status_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.schedule_btn = ctk.CTkButton(self.buttons_frame, text="⏱️ Schedule Task", command=self.open_schedule_window, width=140)
        self.schedule_btn.grid(row=2, column=0, columnspan=3, pady=5)
        self.scheduled_tasks = []
        self.load_schedules()
        self.monitor_schedules()
        self.refresh_status_loop()

    def save_schedules(self):
        with open("scheduled_tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.scheduled_tasks, f, indent=2)

    def load_schedules(self):
        try:
            with open("scheduled_tasks.json", "r", encoding="utf-8") as f:
                self.scheduled_tasks = json.load(f)
        except:
            self.scheduled_tasks = []

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

        # clear and rebuild client buttons
        for widget in self.clients_scroll.winfo_children():
            widget.destroy()

        if isinstance(response, dict) and "error" in response:
            self.status_box.insert("end", f"❌ Error: {response['error']}\n")
        else:
            for client in response:
                client_id = client.get("client_id", "Unknown")
                last_msg = client.get("last_message", "")
                friendly_name = self.client_names.get(client_id, client_id)
                cpu = client.get("cpu", "?")
                ram = client.get("ram", "?")
                disk = client.get("disk", "?")
                display_text = f"{friendly_name}\n🧠 CPU: {cpu}%   💾 RAM: {ram}%   💽 Disk: {disk}%"
                frame = ctk.CTkFrame(self.clients_scroll)
                frame.pack(fill="x", padx=5, pady=2)

                btn = ctk.CTkButton(frame, text=display_text, width=220,
                                    command=lambda cid=client_id: self.select_client(cid))
                btn.pack(side="left", padx=(0, 5))
                self.client_buttons[client_id] = btn

                rename_btn = ctk.CTkButton(frame, text="✏️", width=40,
                                        command=lambda cid=client_id: self.rename_client(cid))
                rename_btn.pack(side="left")

                if last_msg and self.last_messages_seen.get(client_id) != last_msg:
                    self.status_box.insert("end", f"🖥️ {friendly_name}: {last_msg}\n")
                    self.last_messages_seen[client_id] = last_msg

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

    def backup_command(self):
        result = self.controller.broadcast_command("backup_now")
        self.status_box.insert("end", f"💾 {result}\n")


    def refresh_status_loop(self):
        def loop():
            self.refresh_status()
            self.after(REFRESH_INTERVAL * 1000, loop)
        self.after(0, loop)

    def open_schedule_window(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Schedule Task")
        popup.geometry("400x600")

        # Command type
        ctk.CTkLabel(popup, text="Command Type:").pack(pady=5)
        cmd_type = ctk.CTkComboBox(popup, values=["download_selected", "install_selected", "backup_now"])
        cmd_type.set("download_selected")
        cmd_type.pack(pady=5)

        # Program checkboxes
        ctk.CTkLabel(popup, text="Select Programs:").pack(pady=(10, 2))
        prog_frame = ctk.CTkScrollableFrame(popup, height=150)
        prog_frame.pack(pady=2)
        prog_vars = {}
        for prog in PROGRAMS:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(prog_frame, text=prog, variable=var)
            chk.pack(anchor="w")
            prog_vars[prog] = var

        # Client checkboxes
        ctk.CTkLabel(popup, text="Select Target Clients:").pack(pady=(10, 2))
        client_frame = ctk.CTkScrollableFrame(popup, height=150)
        client_frame.pack(pady=2)
        client_vars = {}
        for cid in self.client_names:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(client_frame, text=self.client_names[cid], variable=var)
            chk.pack(anchor="w")
            client_vars[cid] = var

        # Time & Repeat
        ctk.CTkLabel(popup, text="Schedule Time (HH:MM):").pack(pady=5)
        time_entry = ctk.CTkEntry(popup)
        time_entry.insert(0, "14:30")
        time_entry.pack(pady=5)

        repeat_mode = ctk.CTkComboBox(popup, values=["Once", "Daily", "Weekly"])
        repeat_mode.set("Once")
        repeat_mode.pack(pady=5)

        def schedule():
            try:
                when = datetime.datetime.strptime(time_entry.get(), "%H:%M").replace(
                    year=datetime.datetime.now().year,
                    month=datetime.datetime.now().month,
                    day=datetime.datetime.now().day
                )
                now = datetime.datetime.now()
                if when < now:
                    when += datetime.timedelta(days=1)

                # Build command string
                selected_progs = [k for k, v in prog_vars.items() if v.get()]
                cmd = cmd_type.get()
                cmd_str = cmd if cmd == "backup_now" else f"{cmd}:{','.join(selected_progs)}"

                selected_clients = [cid for cid, v in client_vars.items() if v.get()]

                # Save task
                task = {
                    "time": when.strftime("%Y-%m-%d %H:%M"),
                    "command": cmd_str,
                    "clients": selected_clients,
                    "repeat": repeat_mode.get()
                }
                self.scheduled_tasks.append(task)
                self.save_schedules()
                self.status_box.insert("end", f"📅 Scheduled {cmd_str} for {len(selected_clients)} clients at {when.strftime('%H:%M')}\n")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(popup, text="✅ Schedule", command=schedule).pack(pady=10)

    def monitor_schedules(self):
        def monitor():
            while True:
                now = datetime.datetime.now()
                for task in self.scheduled_tasks[:]:
                    task_time = datetime.datetime.strptime(task["time"], "%Y-%m-%d %H:%M")
                    if now >= task_time:
                        cmd = task["command"]
                        repeat = task["repeat"]
                        clients = task["clients"]

                        if clients:
                            for cid in clients:
                                self.controller.send_to_client(cid, cmd)
                                self.status_box.insert("end", f"🚀 Sent to {cid}: {cmd}\n")
                        else:
                            result = self.controller.broadcast_command(cmd)
                            self.status_box.insert("end", f"📡 Broadcast: {cmd} → {result}\n")
                        if repeat == "Daily":
                            task["time"] = (task_time + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
                        elif repeat == "Weekly":
                            task["time"] = (task_time + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d %H:%M")
                        else:
                            self.scheduled_tasks.remove(task)
                        self.save_schedules()
                time.sleep(10)
        threading.Thread(target=monitor, daemon=True).start()

    def load_client_names(self):
        try:
            with open("client_names.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def save_client_names(self):
        with open("client_names.json", "w", encoding="utf-8") as f:
            json.dump(self.client_names, f, indent=2)

    def rename_client(self, client_id):
        popup = ctk.CTkToplevel(self)
        popup.title(f"Rename {client_id}")
        popup.geometry("300x150")

        ctk.CTkLabel(popup, text="New name:").pack(pady=10)
        entry = ctk.CTkEntry(popup)
        entry.insert(0, self.client_names.get(client_id, client_id))
        entry.pack(pady=5)

        def save():
            new_name = entry.get().strip()
            if new_name:
                self.client_names[client_id] = new_name
                self.controller.rename_client(client_id, new_name)
                self.save_client_names()
                self.refresh_status()
                popup.destroy()

        ctk.CTkButton(popup, text="Save", command=save).pack(pady=10)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ClientDashboard()
    app.mainloop()