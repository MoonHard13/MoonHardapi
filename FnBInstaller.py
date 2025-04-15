import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class FnBInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\sunsoftsetups"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_in_registry(self):
        """Αναζήτηση FnB Services σε όλα τα registry paths"""
        locations = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        for root, path in locations:
            try:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "FnB Services" in name:
                                    uninstall_str = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                    return uninstall_str
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return None

    def is_installed(self):
        return self.find_in_registry() is not None

    def uninstall(self):
        """Απεγκαθιστά το FnB Services σιωπηλά με επανεκτέλεση του installer με /uninstall"""
        exe_path = self.find_installer()
        if not exe_path:
            self.log("Δεν βρέθηκε το installer FnB Services για απεγκατάσταση.")
            return
        try:
            self.log(f"Απεγκαθίσταται με: {exe_path} /uninstall /quiet /norestart")
            subprocess.run([
                exe_path,
                "/uninstall",
                "/quiet",
                "/norestart"
            ], check=True)
            self.log("Η σιωπηλή απεγκατάσταση FnB Services ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Σιωπηλής απεγκατάστασης FnB: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης FnB: {e}")

    def find_installer(self):
        """Βρίσκει το .exe αρχείο εγκατάστασης"""
        for root, dirs, files in os.walk(self.base_directory):
            for dir_name in dirs:
                if "FnB Services" in dir_name:
                    for file_name in os.listdir(os.path.join(root, dir_name)):
                        if file_name.lower().endswith(".exe") and "fnb-services" in file_name.lower():
                            return os.path.join(root, dir_name, file_name)
        return None

    def install(self):
        """Κάνει απεγκατάσταση (αν υπάρχει), μετά εγκατάσταση, μετά repair"""
        try:
            if self.is_installed():
                self.uninstall()

            exe_path = self.find_installer()
            if not exe_path:
                self.log("Δεν βρέθηκε το αρχείο εγκατάστασης FnB Services.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το αρχείο εγκατάστασης FnB Services.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "FnB-Install.log")

            self.log(f"Ξεκινά εγκατάσταση FnB Services από: {exe_path}")
            subprocess.run([
                exe_path, "/install", "/quiet", "/norestart", f"/log {temp_log}"
            ], check=True)
            self.log("Η εγκατάσταση FnB Services ολοκληρώθηκε.")

            self.log("Ξεκινά επιδιόρθωση FnB Services...")
            subprocess.run([
                exe_path, "/repair", "/quiet", "/norestart", f"/log {temp_log}"
            ], check=True)
            self.log("Η επιδιόρθωση FnB Services ολοκληρώθηκε.")

            messagebox.showinfo("Επιτυχία", "FnB Services εγκαταστάθηκε και επιδιορθώθηκε με επιτυχία!")

        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάσταση ή επιδιόρθωση FnB: {e}")
            messagebox.showerror("Σφάλμα", f"FnB Services σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα FnB: {e}")
            messagebox.showerror("Σφάλμα", f"Γενικό σφάλμα FnB: {e}")