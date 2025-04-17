import os
import json
import datetime
import pyodbc

class BackupExecutor:
    def __init__(self):
        self.config_path = r"C:\Program Files (x86)\Sunsoft Ltd\ExternalTaxProvider\External.Tax.Provider\appsettings.production.json"
        self.backup_dir = r"C:\SunsoftSetups\BackupDB"
        os.makedirs(self.backup_dir, exist_ok=True)

    def get_connection_string(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["AppSettings"]["BOConnections"][0]["DatabaseConnection"]
        except Exception as e:
            print(f"❌ Σφάλμα ανάγνωσης JSON: {e}")
            return None

    def run_backup(self):
        conn_str = self.get_connection_string()
        if not conn_str:
            print("❌ Δεν βρέθηκε σύνδεση SQL.")
            return

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            db_name = cursor.execute("SELECT DB_NAME()").fetchval()
            date_suffix = datetime.datetime.now().strftime("%d%m%Y")
            backup_file = os.path.join(self.backup_dir, f"{db_name}_{date_suffix}.bak")
            cursor.execute(f"BACKUP DATABASE [{db_name}] TO DISK = N'{backup_file}' WITH FORMAT, INIT")
            conn.commit()
            print(f"✅ Backup ολοκληρώθηκε: {backup_file}")
        except Exception as e:
            print(f"❌ Σφάλμα Backup: {e}")
