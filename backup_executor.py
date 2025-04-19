import os
import json
import re
import datetime
import subprocess
import pyodbc

class BackupExecutor:
    def __init__(self):
        self.appsettings_path = r"C:\Program Files (x86)\Sunsoft Ltd\ExternalTaxProvider\External.Tax.Provider\appsettings.production.json"
        self.backup_dir = r"C:\SunsoftSetups\BackupDB"
        self.connection_params = {}
        os.makedirs(self.backup_dir, exist_ok=True)

    def read_appsettings(self):
        with open(self.appsettings_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        bo_connections = data.get("AppSettings", {}).get("BOConnections", [])
        connection = next((item for item in bo_connections if item.get("ID") == 1), None)
        if not connection:
            raise ValueError("❌ Δεν βρέθηκε σύνδεση με ID=1")

        db_conn_str = connection.get("DatabaseConnection", "")

        self.connection_params['Server'] = re.search(r"Server=([^;]+);", db_conn_str, re.IGNORECASE).group(1)
        self.connection_params['Database'] = re.search(r"Database=([^;]+);", db_conn_str, re.IGNORECASE).group(1)
        self.connection_params['UserID'] = re.search(r"User ID=([^;]+);", db_conn_str, re.IGNORECASE).group(1)
        self.connection_params['Password'] = re.search(r"Password=([^;]+);", db_conn_str, re.IGNORECASE).group(1)

    def run_backup(self):
        try:
            self.read_appsettings()
            server = self.connection_params["Server"]
            database = self.connection_params["Database"]
            backup_file = os.path.join(
                self.backup_dir, f"{database}_{datetime.datetime.now().strftime('%d%m%Y')}.bak"
            )

            print(f"📤 Εκτελείται BACKUP με sqlcmd για τη βάση: {database}")

            sql = f"BACKUP DATABASE [{database}] TO DISK = N'{backup_file}' WITH INIT, COMPRESSION, STATS = 10"

            sqlcmd_command = [
                "sqlcmd",
                "-S", server,
                "-U", self.connection_params["UserID"],
                "-P", self.connection_params["Password"],
                "-Q", sql
            ]

            subprocess.run(sqlcmd_command, check=True)
            print(f"✅ Το backup ολοκληρώθηκε: {backup_file}")

        except Exception as e:
            print(f"❌ Σφάλμα Backup: {e}")
