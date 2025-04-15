<<<<<<< HEAD
import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class WebHookAPIInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Αναζήτηση του WebHookAPI installer"""
        try:
            for dir_name in os.listdir(self.base_directory):
                full_path = os.path.join(self.base_directory, dir_name)
                if os.path.isdir(full_path) and re.match(r'WebHookAPI \d+\.\d+\.\d+\.\d+', dir_name):
                    for file in os.listdir(full_path):
                        if file.lower() == "webhookapi.exe":
                            return os.path.join(full_path, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης WebHookAPI installer: {e}")
        return None

    def is_installed(self):
        """Έλεγχος αν είναι εγκατεστημένο το WebHookAPI"""
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
                                if "WebHookAPI" in name:
                                    return True
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return False

    def uninstall(self):
        """Σιωπηλή απεγκατάσταση με /uninstall"""
        exe_path = self.find_installer()
        if not exe_path:
            self.log("Δεν βρέθηκε το installer WebHookAPI για απεγκατάσταση.")
            return
        try:
            self.log(f"Απεγκαθίσταται με: {exe_path} /uninstall /quiet /norestart")
            subprocess.run([
                exe_path, "/uninstall", "/quiet", "/norestart"
            ], check=True)
            self.log("Η σιωπηλή απεγκατάσταση WebHookAPI ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης WebHookAPI: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης WebHookAPI: {e}")

    def install(self):
        """Εγκατάσταση WebHookAPI σιωπηλά"""
        try:
            if self.is_installed():
                self.uninstall()

            exe_path = self.find_installer()
            if not exe_path:
                self.log("Δεν βρέθηκε το αρχείο εγκατάστασης WebHookAPI.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το αρχείο εγκατάστασης WebHookAPI.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "WebHookAPI-Install.log")

            self.log(f"Ξεκινά εγκατάσταση WebHookAPI από: {exe_path}")
            subprocess.run([
                exe_path, "/install", "/quiet", "/norestart", "/log", temp_log
            ], check=True)
            self.log("Η εγκατάσταση WebHookAPI ολοκληρώθηκε.")
            messagebox.showinfo("Επιτυχία", "Το WebHookAPI εγκαταστάθηκε επιτυχώς.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης WebHookAPI: {e}")
            messagebox.showerror("Σφάλμα", f"WebHookAPI σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα WebHookAPI: {e}")
=======
import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class WebHookAPIInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Αναζήτηση του WebHookAPI installer"""
        try:
            for dir_name in os.listdir(self.base_directory):
                full_path = os.path.join(self.base_directory, dir_name)
                if os.path.isdir(full_path) and re.match(r'WebHookAPI \d+\.\d+\.\d+\.\d+', dir_name):
                    for file in os.listdir(full_path):
                        if file.lower() == "webhookapi.exe":
                            return os.path.join(full_path, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης WebHookAPI installer: {e}")
        return None

    def is_installed(self):
        """Έλεγχος αν είναι εγκατεστημένο το WebHookAPI"""
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
                                if "WebHookAPI" in name:
                                    return True
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return False

    def uninstall(self):
        """Σιωπηλή απεγκατάσταση με /uninstall"""
        exe_path = self.find_installer()
        if not exe_path:
            self.log("Δεν βρέθηκε το installer WebHookAPI για απεγκατάσταση.")
            return
        try:
            self.log(f"Απεγκαθίσταται με: {exe_path} /uninstall /quiet /norestart")
            subprocess.run([
                exe_path, "/uninstall", "/quiet", "/norestart"
            ], check=True)
            self.log("Η σιωπηλή απεγκατάσταση WebHookAPI ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης WebHookAPI: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης WebHookAPI: {e}")

    def install(self):
        """Εγκατάσταση WebHookAPI σιωπηλά"""
        try:
            if self.is_installed():
                self.uninstall()

            exe_path = self.find_installer()
            if not exe_path:
                self.log("Δεν βρέθηκε το αρχείο εγκατάστασης WebHookAPI.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το αρχείο εγκατάστασης WebHookAPI.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "WebHookAPI-Install.log")

            self.log(f"Ξεκινά εγκατάσταση WebHookAPI από: {exe_path}")
            subprocess.run([
                exe_path, "/install", "/quiet", "/norestart", "/log", temp_log
            ], check=True)
            self.log("Η εγκατάσταση WebHookAPI ολοκληρώθηκε.")
            messagebox.showinfo("Επιτυχία", "Το WebHookAPI εγκαταστάθηκε επιτυχώς.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης WebHookAPI: {e}")
            messagebox.showerror("Σφάλμα", f"WebHookAPI σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα WebHookAPI: {e}")
>>>>>>> 791c6b2a0fe9c454ecb508a7d3e37fb9375c839f
            messagebox.showerror("Σφάλμα", f"Γενικό σφάλμα WebHookAPI: {e}")