import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class AMVPMSInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Αναζήτηση του AMVPMSConnectionAPI installer"""
        try:
            for dir_name in os.listdir(self.base_directory):
                full_path = os.path.join(self.base_directory, dir_name)
                if os.path.isdir(full_path) and re.match(r'AMVPMS \d+\.\d+\.\d+', dir_name):
                    for file in os.listdir(full_path):
                        if file.lower() == "amvpmsconnectionapi.exe":
                            return os.path.join(full_path, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης AMVPMS installer: {e}")
        return None

    def is_installed(self):
        """Ελέγχει αν υπάρχει εγκατεστημένο το AMVPMS"""
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
                                if "AMVPMS" in name:
                                    return True
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return False

    def uninstall(self):
        """Silent uninstall μέσω επανεκτέλεσης installer"""
        exe_path = self.find_installer()
        if not exe_path:
            self.log("Δεν βρέθηκε το installer AMVPMS για απεγκατάσταση.")
            return
        try:
            self.log(f"Απεγκαθίσταται με: {exe_path} /uninstall /quiet /norestart")
            subprocess.run([
                exe_path, "/uninstall", "/quiet", "/norestart"
            ], check=True)
            self.log("Η σιωπηλή απεγκατάσταση AMVPMS ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης AMVPMS: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης AMVPMS: {e}")

    def install(self):
        """Εγκατάσταση AMVPMS σιωπηλά"""
        try:
            if self.is_installed():
                self.uninstall()

            exe_path = self.find_installer()
            if not exe_path:
                self.log("Δεν βρέθηκε το αρχείο εγκατάστασης AMVPMS.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το αρχείο εγκατάστασης AMVPMS.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "AMVPMS-Install.log")

            self.log(f"Ξεκινά εγκατάσταση AMVPMS από: {exe_path}")
            subprocess.run([
                exe_path, "/install", "/quiet", "/norestart", "/log", temp_log
            ], check=True)
            self.log("Η εγκατάσταση AMVPMS ολοκληρώθηκε.")
            messagebox.showinfo("Επιτυχία", "Το AMVPMS εγκαταστάθηκε επιτυχώς.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης AMVPMS: {e}")
            messagebox.showerror("Σφάλμα", f"AMVPMS σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα AMVPMS: {e}")
            messagebox.showerror("Σφάλμα", f"Γενικό σφάλμα AMVPMS: {e}")