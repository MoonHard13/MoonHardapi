from program_downloader import ProgramDownloader
from installer_manager import InstallerManager 

class CommandHandler:
    def __init__(self, client, downloader=None):
        self.client = client
        self.downloader = downloader if downloader else ProgramDownloader()
        self.installer = InstallerManager()

    def send(self, msg: str):
        if hasattr(self.client, "message_queue"):
            self.client.message_queue.put_nowait(msg)

    def handle(self, msg: str):
        if msg == "download_all":
            self.downloader.download_programs(list(self.downloader.download_links.keys()))
            self.send("📥 Downloaded all programs")
        elif msg.startswith("download_selected:"):
            programs = [p.strip() for p in msg.split(":", 1)[1].split(",")]
            self.downloader.download_programs(programs)
            self.send(f"📥 Downloaded: {', '.join(programs)}")
        elif msg == "install_all":
            self.installer.install_programs(list(self.installer.mapping.keys()))
            self.send("🛠️ Installed all programs")
        elif msg.startswith("install_selected:"):
            programs = [p.strip() for p in msg.split(":", 1)[1].split(",")]
            self.installer.install_programs(programs)
            self.send(f"🛠️ Installed: {', '.join(programs)}")
        elif msg == "backup_now":
            from backup_executor import BackupExecutor
            BackupExecutor().run_backup()
            self.send("💾 Backup completed")
        else:
            self.send(f"⚠️ Unknown command: {msg}")
