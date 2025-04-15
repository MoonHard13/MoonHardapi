<<<<<<< HEAD
import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class SamtecInstaller:
    def __init__(self, logger_func):
        self.base_path = r"C:\SunsoftSetups\Samtec\setup.exe"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def is_installed(self):
        """Ελέγχει αν είναι εγκατεστημένο το Samtec"""
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
                                if "Samtec" in name or "Technoran" in name:
                                    return True
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return False

    def uninstall(self):
        """Απλή απεγκατάσταση μέσω registry αν βρεθεί UninstallString"""
        try:
            paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            ]
            for root, path in paths:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "Samtec" in name or "Technoran" in name:
                                    uninstall_str = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                    self.log(f"Απεγκαθίσταται με: {uninstall_str} /s /v\"/qn\"")
                                    if uninstall_str.lower().startswith("msiexec"):
                                        command = uninstall_str + " /quiet /norestart"
                                    else:
                                        command = uninstall_str + ' /s /v"/qn"'

                                    self.log(f"Απεγκαθίσταται με: {command}")
                                    subprocess.run(command, shell=True, check=True)
                                    return
                            except FileNotFoundError:
                                continue
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης Samtec: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης Samtec: {e}")

    def install(self):
        """Silent εγκατάσταση Samtec μέσω InstallShield (/s /v"/qn")"""
        try:
            if not os.path.exists(self.base_path):
                self.log("Δεν βρέθηκε το setup.exe του Samtec.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το αρχείο εγκατάστασης Samtec.")
                return

            if self.is_installed():
                self.uninstall()

            log_path = os.path.join(os.environ["TEMP"], "SamtecInstall.log")
            self.log(f"Ξεκινά silent εγκατάσταση Samtec από: {self.base_path}")
            subprocess.run(
                f'"{self.base_path}" /s /v"/qn /l*v \\"{log_path}\\""',
                shell=True,
                check=True
            )
            self.log("Η εγκατάσταση Samtec ολοκληρώθηκε.")
            messagebox.showinfo("Επιτυχία", "Το Samtec εγκαταστάθηκε επιτυχώς.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης Samtec: {e}")
            messagebox.showerror("Σφάλμα", f"Samtec σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα Samtec: {e}")
=======
import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class SamtecInstaller:
    def __init__(self, logger_func):
        self.base_path = r"C:\SunsoftSetups\Samtec\setup.exe"
        self.logger = logger_func

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def is_installed(self):
        """Ελέγχει αν είναι εγκατεστημένο το Samtec"""
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
                                if "Samtec" in name or "Technoran" in name:
                                    return True
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return False

    def uninstall(self):
        """Απλή απεγκατάσταση μέσω registry αν βρεθεί UninstallString"""
        try:
            paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            ]
            for root, path in paths:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "Samtec" in name or "Technoran" in name:
                                    uninstall_str = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                    self.log(f"Απεγκαθίσταται με: {uninstall_str} /s /v\"/qn\"")
                                    if uninstall_str.lower().startswith("msiexec"):
                                        command = uninstall_str + " /quiet /norestart"
                                    else:
                                        command = uninstall_str + ' /s /v"/qn"'

                                    self.log(f"Απεγκαθίσταται με: {command}")
                                    subprocess.run(command, shell=True, check=True)
                                    return
                            except FileNotFoundError:
                                continue
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης Samtec: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης Samtec: {e}")

    def install(self):
        """Silent εγκατάσταση Samtec μέσω InstallShield (/s /v"/qn")"""
        try:
            if not os.path.exists(self.base_path):
                self.log("Δεν βρέθηκε το setup.exe του Samtec.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το αρχείο εγκατάστασης Samtec.")
                return

            if self.is_installed():
                self.uninstall()

            log_path = os.path.join(os.environ["TEMP"], "SamtecInstall.log")
            self.log(f"Ξεκινά silent εγκατάσταση Samtec από: {self.base_path}")
            subprocess.run(
                f'"{self.base_path}" /s /v"/qn /l*v \\"{log_path}\\""',
                shell=True,
                check=True
            )
            self.log("Η εγκατάσταση Samtec ολοκληρώθηκε.")
            messagebox.showinfo("Επιτυχία", "Το Samtec εγκαταστάθηκε επιτυχώς.")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης Samtec: {e}")
            messagebox.showerror("Σφάλμα", f"Samtec σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα Samtec: {e}")
>>>>>>> 791c6b2a0fe9c454ecb508a7d3e37fb9375c839f
            messagebox.showerror("Σφάλμα", f"Γενικό σφάλμα Samtec: {e}")