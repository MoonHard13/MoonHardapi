import os
import subprocess
import socket
import re
from time import sleep
import json, zipfile
from datetime import datetime


# Your predefined ISS templates
ISS_FILES = {
    "server.64.BackOffice Setup-remove.iss": """[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-DlgOrder]
Dlg0={C7974CF7-4574-4485-92D9-C92356FEC0DE}-MessageBox-0
Count=2
Dlg1={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdFinish-0
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-MessageBox-0]
Result=6
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdFinish-0]
Result=1
bOpt1=0
bOpt2=0""",
    "server.64.BackOffice Setup-install.iss": r"""[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-DlgOrder]
Dlg0={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdWelcome-0
Count=9
Dlg1={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdCustomerInfo-0
Dlg2={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdSetupTypeEx-0
Dlg3={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdAskDestPath-0
Dlg4={C7974CF7-4574-4485-92D9-C92356FEC0DE}-MessageBox-0
Dlg5={C7974CF7-4574-4485-92D9-C92356FEC0DE}-MessageBox-1
Dlg6={C7974CF7-4574-4485-92D9-C92356FEC0DE}-LOGON_USER_INFORMATION-0
Dlg7={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdStartCopy-0
Dlg8={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdFinish-0
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdWelcome-0]
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdCustomerInfo-0]
szName=MoonHard
szCompany=.
nvUser=1
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdSetupTypeEx-0]
Result=Single
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdAskDestPath-0]
szDir=C:\Program Files (x86)\Sunsoft Ltd\BackOffice\
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-MessageBox-0]
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-MessageBox-1]
Result=6
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-LOGON_USER_INFORMATION-0]
szAccount=[pcname]\SunAdmin 
szPassword=Sun$up1
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdStartCopy-0]
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdFinish-0]
Result=1
bOpt1=0
bOpt2=0""",
    "server.64.Amvrosia setup-remove.iss": """[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-DlgOrder]
Dlg0={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-MessageBox-0
Count=2
Dlg1={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdFinish-0
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-MessageBox-0]
Result=6
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdFinish-0]
Result=1
bOpt1=0
bOpt2=0""",
    "server.64.Amvrosia setup-install.iss": r"""[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-DlgOrder]
Dlg0={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdWelcome-0
Count=6
Dlg1={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdCustomerInfo-0
Dlg2={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdSetupTypeEx-0
Dlg3={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdAskDestPath-0
Dlg4={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdStartCopy-0
Dlg5={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdFinish-0
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdWelcome-0]
Result=1
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdCustomerInfo-0]
szName=MoonHard
szCompany=.
nvUser=1
Result=1
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdSetupTypeEx-0]
Result=Single
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdAskDestPath-0]
szDir=C:\Program Files (x86)\Sunsoft Ltd\Amvrosia\
Result=1
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdStartCopy-0]
Result=1
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdFinish-0]
Result=1
bOpt1=0
bOpt2=0""",
    "default.64.BackOffice Setup-remove.iss": """[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-DlgOrder]
Dlg0={C7974CF7-4574-4485-92D9-C92356FEC0DE}-MessageBox-0
Count=2
Dlg1={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdFinish-0
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-MessageBox-0]
Result=6
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdFinish-0]
Result=1
bOpt1=0
bOpt2=0""",
    "default.64.BackOffice Setup-install.iss": r"""[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-DlgOrder]
Dlg0={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdWelcome-0
Count=7
Dlg1={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdCustomerInfo-0
Dlg2={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdSetupTypeEx-0
Dlg3={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdAskDestPath-0
Dlg4={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SQLServerSelect-0
Dlg5={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdStartCopy-0
Dlg6={C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdFinish-0
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdWelcome-0]
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdCustomerInfo-0]
szName=MoonHard
szCompany=.
nvUser=1
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdSetupTypeEx-0]
Result=Client
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdAskDestPath-0]
szDir=C:\Program Files (x86)\Sunsoft Ltd\BackOffice\
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SQLServerSelect-0]
szServer=[pcname]
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdStartCopy-0]
Result=1
[{C7974CF7-4574-4485-92D9-C92356FEC0DE}-SdFinish-0]
Result=1
bOpt1=0
bOpt2=0""",
    "default.64.Amvrosia setup-remove.iss": """[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-DlgOrder]
Dlg0={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-MessageBox-0
Count=2
Dlg1={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdFinish-0
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-MessageBox-0]
Result=6
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdFinish-0]
Result=1
bOpt1=0
bOpt2=0""",
    "default.64.Amvrosia setup-install.iss": r"""[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-DlgOrder]
Dlg0={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdWelcome-0
Count=6
Dlg1={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdCustomerInfo-0
Dlg2={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdSetupTypeEx-0
Dlg3={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdAskDestPath-0
Dlg4={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdStartCopy-0
Dlg5={2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdFinish-0
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdWelcome-0]
Result=1
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdCustomerInfo-0]
szName=MoonHard
szCompany=.
nvUser=1
Result=1
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdSetupTypeEx-0]
Result=Client
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdAskDestPath-0]
szDir=C:\Program Files (x86)\Sunsoft Ltd\Amvrosia\
Result=1
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdStartCopy-0]
Result=1
[{2B77D814-2D96-4FAE-9D85-7AD1D5E2023C}-SdFinish-0]
Result=1
bOpt1=0
bOpt2=0""",
}

class MainAppsInstaller:
    def __init__(self, logger_func):
        self.logger = logger_func
        self.setup_dir = r"C:\SunsoftSetups"
        self.full_update_cmd = os.path.join(self.setup_dir, "FullUpdateServer.cmd")
        self.updater_exe = os.path.join(self.setup_dir, "SunsoftUpdater.v.2.1.0.0.exe")

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def install(self):
        # === Βήμα 0: Κλείσιμο εφαρμογών ===
        processes_to_kill = [
            "S1 Connector.exe", "dllhost.exe", "FiscalService.exe",
            "POSSystem.exe", "BOffice.exe", "Amvrosia.exe"
        ]
        self.log("🛑 Κλείσιμο σχετικών εφαρμογών...")
        for proc in processes_to_kill:
            try:
                subprocess.run(f'taskkill /f /im "{proc}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.log(f"✅ Έκλεισε: {proc}")
            except Exception as e:
                self.log(f"[Σφάλμα] Κλείνοντας {proc}: {e}")

        # === Βήμα 1: Εκτέλεση SunsoftUpdater αν δεν υπάρχει FullUpdateServer.cmd ===
        if not os.path.exists(self.full_update_cmd):
            self.log("⚠️ FullUpdateServer.cmd δεν βρέθηκε. Εκτελείται SunsoftUpdater...")
            try:
                subprocess.run(f'"{self.updater_exe}"', check=True, shell=True, cwd=self.setup_dir)
                self.log("✅ Εκτελέστηκε SunsoftUpdater.")
            except Exception as e:
                self.log(f"[Σφάλμα] Εκτέλεση SunsoftUpdater: {e}")

        # === Βήμα 2: Δημιουργία .iss ===
        domain_name = socket.getfqdn()
        missing_files = []
        for filename in ISS_FILES.keys():
            dest = os.path.join(self.setup_dir, filename)
            if not os.path.exists(dest):
                missing_files.append(filename)

        if missing_files:
            self.log("📄 Δημιουργία αρχείων .iss...")
            for filename in missing_files:
                dest = os.path.join(self.setup_dir, filename)
                try:
                    updated_content = ISS_FILES[filename].replace("[pcname]", domain_name)
                    with open(dest, "w", encoding="utf-8") as f:
                        f.write(updated_content)
                    self.log(f"✅ Δημιουργήθηκε: {filename}")
                except Exception as e:
                    self.log(f"[Σφάλμα] Δημιουργίας {filename}: {e}")
        else:
            self.log("ℹ️ Τα αρχεία .iss υπάρχουν ήδη.")

        # === Βήμα X: SQL Backup ===
        try:
            self.log("💾 Δημιουργία backup SQL βάσης από appsettings.production.json...")
            json_path = r"C:\\Program Files (x86)\\Sunsoft Ltd\\ExternalTaxProvider\\External.Tax.Provider\\appsettings.production.json"
            with open(json_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            bo_connections = config_data.get("AppSettings", {}).get("BOConnections", [])
            connection = next((item for item in bo_connections if item.get("ID") == 1), None)
            if not connection:
                raise ValueError("❌ Δεν βρέθηκε σύνδεση με ID=1")

            db_conn_str = connection.get("DatabaseConnection", "")

            server = re.search(r"Server=([^;]+);", db_conn_str, re.IGNORECASE).group(1)
            database = re.search(r"Database=([^;]+);", db_conn_str, re.IGNORECASE).group(1)
            user = re.search(r"User ID=([^;]+);", db_conn_str, re.IGNORECASE).group(1)
            password = re.search(r"Password=([^;]+);", db_conn_str, re.IGNORECASE).group(1)

            date = datetime.now().strftime("%d%m%Y")
            backup_dir = r"C:\\SunsoftSetups\\BackupDB"
            os.makedirs(backup_dir, exist_ok=True)
            bak_file = os.path.join(backup_dir, f"{database}_{date}.bak")

            self.log(f"📤 Εκτελείται BACKUP για βάση: {database}...")

            sql = f"BACKUP DATABASE [{database}] TO DISK = N'{bak_file}' WITH INIT, COMPRESSION, STATS = 10"
            sqlcmd_command = [
                "sqlcmd",
                "-S", server,
                "-U", user,
                "-P", password,
                "-Q", sql
            ]

            subprocess.run(sqlcmd_command, check=True)
            self.log(f"✅ Το backup ολοκληρώθηκε: {bak_file}")

        except Exception as e:
            self.log(f"[Σφάλμα] Δημιουργίας backup: {e}")


        # === Βήμα 3: Εκτέλεση FullUpdateServer.cmd ===
        try:
            self.log("🚀 Εκτελείται FullUpdateServer.cmd...")
            subprocess.run(self.full_update_cmd, check=True, shell=True, cwd=self.setup_dir)
            self.log("✅ Ολοκληρώθηκε το Full Update.")
        except Exception as e:
            self.log(f"[Σφάλμα] Εκτέλεσης FullUpdateServer.cmd: {e}")

        # === Βήμα 4: Εκτέλεση UpgradeDb.exe ===
        self.run_upgrade_db()

    def run_upgrade_db(self):
        exe_path = r"C:\\Program Files (x86)\\Common Files\\Sunsoft\\UpgradeDb.exe"

        applications = {
            "BackOffice": "2",  # Επιλογή 2 για BackOffice
            "Amvrosia": "1"     # Επιλογή 1 για Amvrosia
        }

        try:
            for app_name, app_number in applications.items():
                self.log(f"🔄 Ξεκινά UpgradeDb για εφαρμογή: {app_name}...")

                inputs = f"{app_number}\n2\n0\n0\n"  # Επιλογή εφαρμογής ➔ Επιλογή βάσης ➔ Exit ➔ Exit

                proc = subprocess.Popen(
                    [exe_path, "-i"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=r"C:\Program Files (x86)\Common Files\Sunsoft"
                )

                output, error = proc.communicate(input=inputs)

                self.log(f"[UpgradeDb] Έξοδος για {app_name}:")
                for line in output.splitlines():
                    self.log(f"[UpgradeDb] {line.strip()}")

                if proc.returncode == 0:
                    self.log(f"✅ Ολοκληρώθηκε το UpgradeDb για {app_name} χωρίς σφάλματα.")
                else:
                    self.log(f"❌ Σφάλμα στο UpgradeDb για {app_name}. Κωδικός εξόδου: {proc.returncode}")

        except Exception as e:
            self.log(f"❌ Εξαίρεση στην εκτέλεση UpgradeDb: {e}")



        
        

