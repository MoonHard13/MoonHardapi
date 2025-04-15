<<<<<<< HEAD
import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class CallServerHostInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Βρίσκει το CallServer Host .msi"""
        try:
            for file in os.listdir(self.base_directory):
                if re.match(r'CallServer Host \d+\.\d+\.\d+\.\d+\.msi', file):
                    return os.path.join(self.base_directory, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης Host MSI: {e}")
        return None

    def is_installed(self):
        """Ελέγχει αν υπάρχει εγκατεστημένο το CallServer Host"""
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
                                if "CallServer Host" in name:
                                    return subkey_name
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return None

    def uninstall(self):
        product_code = self.is_installed()
        if not product_code:
            self.log("Δεν βρέθηκε εγκατεστημένο CallServer Host.")
            return
        try:
            self.log(f"Απεγκαθίσταται με GUID: {product_code}")
            subprocess.run(["msiexec", "/x", product_code, "/quiet", "/norestart"], check=True)
            self.log("Η σιωπηλή απεγκατάσταση CallServer Host ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης Host: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης Host: {e}")

    def install(self):
        try:
            if self.is_installed():
                self.uninstall()

            msi_path = self.find_installer()
            if not msi_path:
                self.log("Δεν βρέθηκε το MSI του CallServer Host.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το MSI του CallServer Host.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "CallServerHost-Install.log")
            self.log(f"Ξεκινά εγκατάσταση CallServer Host από: {msi_path}")
            subprocess.run([
                "msiexec", "/i", msi_path, "/quiet", "/norestart", "/l*v", temp_log
            ], check=True)
            self.log("Η εγκατάσταση CallServer Host ολοκληρώθηκε.")
            messagebox.showinfo("Επιτυχία", "Το CallServer Host εγκαταστάθηκε επιτυχώς.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης Host: {e}")
            messagebox.showerror("Σφάλμα", f"CallServer Host σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα Host: {e}")
=======
import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class CallServerHostInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Βρίσκει το CallServer Host .msi"""
        try:
            for file in os.listdir(self.base_directory):
                if re.match(r'CallServer Host \d+\.\d+\.\d+\.\d+\.msi', file):
                    return os.path.join(self.base_directory, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης Host MSI: {e}")
        return None

    def is_installed(self):
        """Ελέγχει αν υπάρχει εγκατεστημένο το CallServer Host"""
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
                                if "CallServer Host" in name:
                                    return subkey_name
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return None

    def uninstall(self):
        product_code = self.is_installed()
        if not product_code:
            self.log("Δεν βρέθηκε εγκατεστημένο CallServer Host.")
            return
        try:
            self.log(f"Απεγκαθίσταται με GUID: {product_code}")
            subprocess.run(["msiexec", "/x", product_code, "/quiet", "/norestart"], check=True)
            self.log("Η σιωπηλή απεγκατάσταση CallServer Host ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης Host: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης Host: {e}")

    def install(self):
        try:
            if self.is_installed():
                self.uninstall()

            msi_path = self.find_installer()
            if not msi_path:
                self.log("Δεν βρέθηκε το MSI του CallServer Host.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το MSI του CallServer Host.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "CallServerHost-Install.log")
            self.log(f"Ξεκινά εγκατάσταση CallServer Host από: {msi_path}")
            subprocess.run([
                "msiexec", "/i", msi_path, "/quiet", "/norestart", "/l*v", temp_log
            ], check=True)
            self.log("Η εγκατάσταση CallServer Host ολοκληρώθηκε.")
            messagebox.showinfo("Επιτυχία", "Το CallServer Host εγκαταστάθηκε επιτυχώς.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης Host: {e}")
            messagebox.showerror("Σφάλμα", f"CallServer Host σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα Host: {e}")
>>>>>>> 791c6b2a0fe9c454ecb508a7d3e37fb9375c839f
            messagebox.showerror("Σφάλμα", f"Γενικό σφάλμα CallServer Host: {e}")