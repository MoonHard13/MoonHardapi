import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class StatisticsInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Αναζήτηση MSI του Sunsoft Statistics"""
        try:
            for dir_name in os.listdir(self.base_directory):
                full_path = os.path.join(self.base_directory, dir_name)
                if os.path.isdir(full_path) and re.match(r'Statistics \d+\.\d+\.\d+', dir_name):
                    for file in os.listdir(full_path):
                        if re.match(r'Sunsoft Statistics \d+\.\d+\.\d+\.\d+\.msi', file):
                            return os.path.join(full_path, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης Statistics MSI: {e}")
        return None

    def is_installed(self):
        """Ελέγχει αν υπάρχει εγκατεστημένο το Statistics"""
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
                                if "Sunsoft Statistics" in name:
                                    return subkey_name  # Return ProductCode (GUID)
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return None

    def uninstall(self):
        """Silent uninstall με msiexec /x {ProductCode}"""
        product_code = self.is_installed()
        if not product_code:
            self.log("Δεν βρέθηκε εγκατεστημένο Statistics για απεγκατάσταση.")
            return
        try:
            self.log(f"Απεγκαθίσταται με GUID: {product_code}")
            subprocess.run([
                "msiexec", "/x", product_code, "/quiet", "/norestart"
            ], check=True)
            self.log("Η σιωπηλή απεγκατάσταση Sunsoft Statistics ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης Statistics: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης Statistics: {e}")

    def install(self):
        """Εγκατάσταση του Sunsoft Statistics μέσω MSI"""
        try:
            if self.is_installed():
                self.uninstall()

            msi_path = self.find_installer()
            if not msi_path:
                self.log("Δεν βρέθηκε το MSI installer του Sunsoft Statistics.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το αρχείο εγκατάστασης Sunsoft Statistics.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "Statistics-Install.log")

            self.log(f"Ξεκινά εγκατάσταση Sunsoft Statistics από: {msi_path}")
            subprocess.run([
                "msiexec", "/i", msi_path, "/quiet", "/norestart", "/l*v", temp_log
            ], check=True)
            self.log("Η εγκατάσταση Sunsoft Statistics ολοκληρώθηκε.")
            messagebox.showinfo("Επιτυχία", "Το Sunsoft Statistics εγκαταστάθηκε επιτυχώς.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης Statistics: {e}")
            messagebox.showerror("Σφάλμα", f"Statistics σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα Statistics: {e}")
            messagebox.showerror("Σφάλμα", f"Γενικό σφάλμα Statistics: {e}")