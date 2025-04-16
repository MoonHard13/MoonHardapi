import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class ProviderInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Αναζήτηση του ExternalTaxProvider installer"""
        try:
            for dir_name in os.listdir(self.base_directory):
                full_path = os.path.join(self.base_directory, dir_name)
                if os.path.isdir(full_path) and re.match(r'Provider \d+\.\d+\.\d+\.\d+', dir_name):
                    for file in os.listdir(full_path):
                        if re.match(r'ExternalTaxProvider\.\d+\.\d+\.\d+\.\d+\.exe', file):
                            return os.path.join(full_path, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης Provider installer: {e}")
        return None

    def is_installed(self):
        """Ελέγχει αν υπάρχει εγκατεστημένος Provider (ευέλικα)"""
        paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        for root, path in paths:
            try:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "External Tax Provider" in name:
                                    return True
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return False

    def uninstall(self):
        """Επανεκτελεί το installer με /uninstall για silent απεγκατάσταση"""
        exe_path = self.find_installer()
        if not exe_path:
            self.log("Δεν βρέθηκε το installer Provider για απεγκατάσταση.")
            return
        try:
            self.log(f"Απεγκαθίσταται με: {exe_path} /uninstall /quiet /norestart")
            subprocess.run([
                exe_path, "/uninstall", "/quiet", "/norestart"
            ], check=True)
            self.log("Η σιωπηλή απεγκατάσταση Provider ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης Provider: {e}")

    def install(self):
        """Εγκαθιστά τον External Tax Provider σιωπηλά"""
        try:
            if self.is_installed():
                self.uninstall()

            exe_path = self.find_installer()
            if not exe_path:
                self.log("Δεν βρέθηκε το αρχείο εγκατάστασης External Tax Provider.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "Provider-Install.log")

            self.log(f"Ξεκινά εγκατάσταση External Tax Provider από: {exe_path}")
            subprocess.run([
                exe_path, "/install", "/quiet", "/norestart", f"/log", temp_log
            ], check=True)
            self.log("Η εγκατάσταση External Tax Provider ολοκληρώθηκε.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης Provider: {e}")
            messagebox.showerror("Σφάλμα", f"External Tax Provider σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα Provider: {e}")