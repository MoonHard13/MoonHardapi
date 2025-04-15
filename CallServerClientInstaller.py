import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class CallServerClientInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Βρίσκει το CallServer Client .msi"""
        try:
            for file in os.listdir(self.base_directory):
                if re.match(r'CallServer Client \d+\.\d+\.\d+\.\d+\.msi', file):
                    return os.path.join(self.base_directory, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης Client MSI: {e}")
        return None

    def is_installed(self):
        """Ελέγχει αν υπάρχει εγκατεστημένο το CallServer Client"""
        paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        for root, path in paths:
            try:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "CallServer Client" in name:
                                    return subkey_name
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return None

    def uninstall(self):
        product_code = self.is_installed()
        if not product_code:
            self.log("Δεν βρέθηκε εγκατεστημένο CallServer Client.")
            return
        try:
            self.log(f"Απεγκαθίσταται με GUID: {product_code}")
            subprocess.run(["msiexec", "/x", product_code, "/quiet", "/norestart"], check=True)
            self.log("Η σιωπηλή απεγκατάσταση CallServer Client ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης Client: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης Client: {e}")

    def install(self):
        try:
            if self.is_installed():
                self.uninstall()

            msi_path = self.find_installer()
            if not msi_path:
                self.log("Δεν βρέθηκε το MSI του CallServer Client.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το MSI του CallServer Client.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "CallServerClient-Install.log")
            self.log(f"Ξεκινά εγκατάσταση CallServer Client από: {msi_path}")
            subprocess.run([
                "msiexec", "/i", msi_path, "/quiet", "/norestart", "/l*v", temp_log
            ], check=True)
            self.log("Η εγκατάσταση CallServer Client ολοκληρώθηκε.")
            messagebox.showinfo("Επιτυχία", "Το CallServer Client εγκαταστάθηκε επιτυχώς.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης Client: {e}")
            messagebox.showerror("Σφάλμα", f"CallServer Client σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα Client: {e}")
            messagebox.showerror("Σφάλμα", f"Γενικό σφάλμα CallServer Client: {e}")