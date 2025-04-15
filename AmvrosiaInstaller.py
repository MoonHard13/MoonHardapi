<<<<<<< HEAD
import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class AmvrosiaInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.apk_subdir = "Waiter"
        self.logger = logger_func
        self.apk_dest = r"C:\Program Files (x86)\Sunsoft Ltd\AmvrosiaWebService\Amvrosia.Web.Service\DL\Files"

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Αναζήτηση MSI installer σε φάκελο AmvrosiaService *.*.*"""
        try:
            for dir_name in os.listdir(self.base_directory):
                full_path = os.path.join(self.base_directory, dir_name)
                if os.path.isdir(full_path) and re.match(r'AmvrosiaService \d+\.\d+\.\d+', dir_name):
                    for file in os.listdir(full_path):
                        if re.match(r'Amvrosia Web Service \d+\.\d+\.\d+\.\d+\.msi', file):
                            return os.path.join(full_path, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης MSI: {e}")
        return None

    def find_product_guid(self):
        """Εντοπισμός GUID από registry για silent uninstall"""
        uninstall_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        for root, path in uninstall_paths:
            try:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "Amvrosia Web Service" in name:
                                    return subkey_name
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return None

    def is_installed(self):
        return self.find_product_guid() is not None

    def uninstall(self):
        """Silent uninstall μέσω GUID"""
        product_guid = self.find_product_guid()
        if not product_guid:
            self.log("Δεν βρέθηκε εγκατεστημένο Amvrosia Web Service.")
            return
        try:
            self.log(f"Απεγκαθίσταται με GUID: {product_guid}")
            subprocess.run([
                "msiexec", "/x", f"{product_guid}", "/quiet", "/norestart"
            ], check=True)
            self.log("Η σιωπηλή απεγκατάσταση Amvrosia Web Service ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης Amvrosia: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης: {e}")

    def replace_apk(self, msi_path):
        """Αντικαθιστά το AmvrosiaMobile.apk από το φάκελο Waiter που είναι δίπλα στο MSI"""
        try:
            base_folder = os.path.dirname(msi_path)
            waiter_dir = os.path.join(base_folder, "Waiter")
            if not os.path.exists(waiter_dir):
                self.log(f"[Σφάλμα] Δεν βρέθηκε φάκελος Waiter: {waiter_dir}")
                return

            # Βρες το .apk αρχείο
            for file in os.listdir(waiter_dir):
                if re.match(r'AmvrosiaMobile\.\d+\.\d+\.\d+\.apk', file):
                    src_apk = os.path.join(waiter_dir, file)
                    dest_apk = os.path.join(self.apk_dest, "AmvrosiaMobile.apk")

                    # Διαγραφή όλων των .apk στον προορισμό
                    for f in os.listdir(self.apk_dest):
                        if f.lower().endswith(".apk"):
                            os.remove(os.path.join(self.apk_dest, f))
                            self.log(f"Διαγράφηκε παλιό APK: {f}")

                    shutil.copy(src_apk, dest_apk)
                    self.log(f"Αντικαταστάθηκε το APK: {src_apk} → {dest_apk}")
                    return

            self.log("Δεν βρέθηκε αρχείο AmvrosiaMobile.apk μέσα στο φάκελο Waiter.")
        except Exception as e:
            self.log(f"[Σφάλμα] Αντικατάστασης APK: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία APK αντιγραφής: {e}")

    def install(self):
        """Κύρια εγκατάσταση με silent MSI + αντικατάσταση APK"""
        try:
            if self.is_installed():
                self.uninstall()

            msi_path = self.find_installer()
            if not msi_path:
                self.log("Δεν βρέθηκε το αρχείο εγκατάστασης Amvrosia Web Service.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το αρχείο εγκατάστασης Amvrosia Web Service.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "Amvrosia-Install.log")

            self.log(f"Ξεκινά εγκατάσταση Amvrosia Web Service από: {msi_path}")
            subprocess.run([
                "msiexec", "/i", msi_path, "/quiet", "/norestart", "/l*v", temp_log
            ], check=True)

            self.log("Η εγκατάσταση Amvrosia Web Service ολοκληρώθηκε.")

            self.replace_apk(msi_path)

            messagebox.showinfo("Επιτυχία", "Amvrosia Web Service εγκαταστάθηκε και ενημερώθηκε το APK!")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης Amvrosia: {e}")
            messagebox.showerror("Σφάλμα", f"Amvrosia Web Service σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα Amvrosia: {e}")
=======
import os, subprocess, time, re, shutil
import winreg
from tkinter import messagebox

class AmvrosiaInstaller:
    def __init__(self, logger_func):
        self.base_directory = r"C:\SunsoftSetups"
        self.apk_subdir = "Waiter"
        self.logger = logger_func
        self.apk_dest = r"C:\Program Files (x86)\Sunsoft Ltd\AmvrosiaWebService\Amvrosia.Web.Service\DL\Files"

    def log(self, msg):
        if self.logger:
            self.logger(msg)

    def find_installer(self):
        """Αναζήτηση MSI installer σε φάκελο AmvrosiaService *.*.*"""
        try:
            for dir_name in os.listdir(self.base_directory):
                full_path = os.path.join(self.base_directory, dir_name)
                if os.path.isdir(full_path) and re.match(r'AmvrosiaService \d+\.\d+\.\d+', dir_name):
                    for file in os.listdir(full_path):
                        if re.match(r'Amvrosia Web Service \d+\.\d+\.\d+\.\d+\.msi', file):
                            return os.path.join(full_path, file)
        except Exception as e:
            self.log(f"[Σφάλμα] Εύρεσης MSI: {e}")
        return None

    def find_product_guid(self):
        """Εντοπισμός GUID από registry για silent uninstall"""
        uninstall_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        for root, path in uninstall_paths:
            try:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "Amvrosia Web Service" in name:
                                    return subkey_name
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
        return None

    def is_installed(self):
        return self.find_product_guid() is not None

    def uninstall(self):
        """Silent uninstall μέσω GUID"""
        product_guid = self.find_product_guid()
        if not product_guid:
            self.log("Δεν βρέθηκε εγκατεστημένο Amvrosia Web Service.")
            return
        try:
            self.log(f"Απεγκαθίσταται με GUID: {product_guid}")
            subprocess.run([
                "msiexec", "/x", f"{product_guid}", "/quiet", "/norestart"
            ], check=True)
            self.log("Η σιωπηλή απεγκατάσταση Amvrosia Web Service ολοκληρώθηκε.")
            time.sleep(5)
        except Exception as e:
            self.log(f"[Σφάλμα] Απεγκατάστασης Amvrosia: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία απεγκατάστασης: {e}")

    def replace_apk(self, msi_path):
        """Αντικαθιστά το AmvrosiaMobile.apk από το φάκελο Waiter που είναι δίπλα στο MSI"""
        try:
            base_folder = os.path.dirname(msi_path)
            waiter_dir = os.path.join(base_folder, "Waiter")
            if not os.path.exists(waiter_dir):
                self.log(f"[Σφάλμα] Δεν βρέθηκε φάκελος Waiter: {waiter_dir}")
                return

            # Βρες το .apk αρχείο
            for file in os.listdir(waiter_dir):
                if re.match(r'AmvrosiaMobile\.\d+\.\d+\.\d+\.apk', file):
                    src_apk = os.path.join(waiter_dir, file)
                    dest_apk = os.path.join(self.apk_dest, "AmvrosiaMobile.apk")

                    # Διαγραφή όλων των .apk στον προορισμό
                    for f in os.listdir(self.apk_dest):
                        if f.lower().endswith(".apk"):
                            os.remove(os.path.join(self.apk_dest, f))
                            self.log(f"Διαγράφηκε παλιό APK: {f}")

                    shutil.copy(src_apk, dest_apk)
                    self.log(f"Αντικαταστάθηκε το APK: {src_apk} → {dest_apk}")
                    return

            self.log("Δεν βρέθηκε αρχείο AmvrosiaMobile.apk μέσα στο φάκελο Waiter.")
        except Exception as e:
            self.log(f"[Σφάλμα] Αντικατάστασης APK: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία APK αντιγραφής: {e}")

    def install(self):
        """Κύρια εγκατάσταση με silent MSI + αντικατάσταση APK"""
        try:
            if self.is_installed():
                self.uninstall()

            msi_path = self.find_installer()
            if not msi_path:
                self.log("Δεν βρέθηκε το αρχείο εγκατάστασης Amvrosia Web Service.")
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε το αρχείο εγκατάστασης Amvrosia Web Service.")
                return

            temp_log = os.path.join(os.environ["TEMP"], "Amvrosia-Install.log")

            self.log(f"Ξεκινά εγκατάσταση Amvrosia Web Service από: {msi_path}")
            subprocess.run([
                "msiexec", "/i", msi_path, "/quiet", "/norestart", "/l*v", temp_log
            ], check=True)

            self.log("Η εγκατάσταση Amvrosia Web Service ολοκληρώθηκε.")

            self.replace_apk(msi_path)

            messagebox.showinfo("Επιτυχία", "Amvrosia Web Service εγκαταστάθηκε και ενημερώθηκε το APK!")
        except subprocess.CalledProcessError as e:
            self.log(f"[Σφάλμα] Εγκατάστασης Amvrosia: {e}")
            messagebox.showerror("Σφάλμα", f"Amvrosia Web Service σφάλμα: {e}")
        except Exception as e:
            self.log(f"[Σφάλμα] Γενικό σφάλμα Amvrosia: {e}")
>>>>>>> 791c6b2a0fe9c454ecb508a7d3e37fb9375c839f
            messagebox.showerror("Σφάλμα", f"Γενικό σφάλμα Amvrosia: {e}")