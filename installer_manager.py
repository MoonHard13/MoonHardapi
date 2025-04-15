import logging
from FnBInstaller import FnBInstaller
from AmvrosiaInstaller import AmvrosiaInstaller
from ProviderInstaller import ProviderInstaller
from SnServiceInstaller import SnServiceInstaller
from AMVPMSInstaller import AMVPMSInstaller
from ExternalConnectionInstaller import ExternalConnectionInstaller
from WebHookAPIInstaller import WebHookAPIInstaller
from StatisticsInstaller import StatisticsInstaller
from CallServerHostInstaller import CallServerHostInstaller
from CallServerClientInstaller import CallServerClientInstaller
from SamtecInstaller import SamtecInstaller
from MainAppsInstaller import MainAppsInstaller


class InstallerManager:
    def __init__(self):
        self.logger = logging.getLogger("InstallerManager")
        self.logger.setLevel(logging.INFO)
        self.mapping = {
            "FnB Services": FnBInstaller,
            "Amvrosia Service": AmvrosiaInstaller,
            "External Provider": ProviderInstaller,
            "SnService": SnServiceInstaller,
            "AMVPMS": AMVPMSInstaller,
            "External Con API": ExternalConnectionInstaller,
            "WebHookAPI": WebHookAPIInstaller,
            "Statistics": StatisticsInstaller,
            "CallServer Host": CallServerHostInstaller,
            "CallServer Client": CallServerClientInstaller,
            "Samtec": SamtecInstaller,
            "Main Apps": MainAppsInstaller,
        }

    def log(self, msg):
        print(msg)
        self.logger.info(msg)

    def install_programs(self, program_list):
        for name in program_list:
            installer_class = self.mapping.get(name.strip())
            if installer_class:
                try:
                    self.log(f"🚀 Εγκατάσταση: {name}")
                    installer = installer_class(logger_func=self.log)
                    installer.install()
                    self.log(f"✅ Ολοκληρώθηκε: {name}")
                except Exception as e:
                    self.log(f"❌ Αποτυχία εγκατάστασης {name}: {e}")
            else:
                self.log(f"⚠️ Δεν υπάρχει installer για: {name}")