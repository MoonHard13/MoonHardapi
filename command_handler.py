from program_downloader import ProgramDownloader
from installer_manager import InstallerManager 

class CommandHandler:
    def __init__(self, client):
        self.client = client
        self.downloader = ProgramDownloader()
        self.installer = InstallerManager()

    def handle(self, msg: str):
        if msg == "download_all":
            self.downloader.download_programs(list(self.downloader.download_links.keys()))
            print("✅ Downloaded all programs")
        elif msg.startswith("download_selected:"):
            programs = [p.strip() for p in msg.split(":", 1)[1].split(",")]
            self.downloader.download_programs(programs)
            print(f"✅ Download triggered for: {', '.join(programs)}")
        elif msg == "install_all":
            self.installer.install_programs(list(self.installer.mapping.keys()))
            print("✅ Installed all programs")
        elif msg.startswith("install_selected:"):
            programs = [p.strip() for p in msg.split(":", 1)[1].split(",")]
            self.installer.install_programs(programs)
            print(f"✅ Install triggered for: {', '.join(programs)}")
        else:
            print(f"⚠️ Unknown command: {msg}")
