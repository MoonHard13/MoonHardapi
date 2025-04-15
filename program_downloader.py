import os
import logging
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class ProgramDownloader:
    def __init__(self):
        self.download_links = {
            "Amvrosia Service": "https://drive.google.com/drive/folders/1LFaI84SbgPdTAGfkN1VKi8znqShpG_VV",
            "SnService": "https://drive.google.com/drive/folders/1zh10RewQXVAVsqFshpy8Kd6s8v88czfQ",
            "CallServer Host": "https://drive.google.com/drive/folders/19o044imDR6DlHeY3h_7zcMUx8kSSE6N4",
            "CallServer Client": "https://drive.google.com/drive/folders/1T3tQs4xdY1Ld0yvAuJVCvTirKJtlLdhM",
            "External Provider": "https://drive.google.com/drive/folders/1tb477TDcTyufjab3VbSpu1l1Qfa60MJI",
            "FnB Services": "https://drive.google.com/drive/folders/10nQSyoHzR45kyYhwLGWfMPRtvD4WBQaa",
            "AMVPMS": "https://drive.google.com/drive/folders/1Vn6zgrrxD-3KbPYKnKe-4-Ui5VCktrhM",
            "WebHookAPI": "https://drive.google.com/drive/folders/1T8O6xjke_5VLz7TfiiqyLMoRx9-QvFns",
            "External Con API": "https://drive.google.com/drive/folders/1_kHDaukj4E0GwRCJY2tXmhqAFMO-V4_l",
            "Main Apps": "https://drive.google.com/drive/folders/18I6QjSLxpXanFIvQwI5_3bXSX3ohBj6D",
            "Statistics": "https://drive.google.com/drive/folders/14VNTSiHMql9EcOyoO_71kM29iCbFytmi",
            "Samtec": "https://drive.google.com/drive/folders/1ZqbwrULhAOKsUmbnVzJrk_U2UOirDZ0C",
            "Copy S1DC": "https://drive.google.com/drive/folders/1SV7WVJka1Ux9Cz1NracRmPqXIR-Lnh7S"
        }

        self.download_dir = r"C:\SunsoftSetups"
        self.base_dir = os.path.join(self.download_dir, "MoonHardRemote")

        print("🛠 Creating and checking paths:", self.download_dir, self.base_dir)

        self.ensure_directories()
        self.logger = self.setup_logger()
        self.drive = self.authenticate_drive()

    def ensure_directories(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            os.system(f'attrib -R "{self.download_dir}"')
            os.system(f'net share SunsoftSetups="{self.download_dir}" /GRANT:Everyone,FULL')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        client_secrets_path = os.path.join(self.base_dir, "client_secrets.json")
        if not os.path.exists(client_secrets_path):
            from shutil import copyfile
            copyfile("client_secrets.json", client_secrets_path)

    def setup_logger(self):
        log_path = os.path.join(self.base_dir, "program_downloader.log")
        logging.basicConfig(
            filename=log_path,
            filemode='a',
            format='%(asctime)s | %(levelname)s | %(message)s',
            level=logging.INFO,
            encoding='utf-8'
        )
        return logging.getLogger("ProgramDownloader")

    def authenticate_drive(self):
        creds_path = os.path.join(self.base_dir, "mycreds.txt")
        secrets_path = os.path.join(self.base_dir, "client_secrets.json")

        gauth = GoogleAuth()
        gauth.LoadClientConfigFile(secrets_path)

        if not os.path.exists(creds_path):
            print("🔐 First-time auth: opening browser to authenticate...")
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile(creds_path)
            return GoogleDrive(gauth)

        gauth.LoadCredentialsFile(creds_path)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile(creds_path)
        return GoogleDrive(gauth)

    def download_programs(self, program_list):
        print("🚀 download_programs called with:", program_list)
        for program in program_list:
            link = self.download_links.get(program)
            if not link:
                msg = f"⚠️ Unknown program: {program}"
                print(msg)
                self.logger.warning(msg)
                continue

            folder_id = self.extract_folder_id(link)
            if not folder_id:
                msg = f"❌ Could not extract folder ID for {program}"
                print(msg)
                self.logger.error(msg)
                continue

            file_list = self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
            for file in file_list:
                file_path = os.path.join(self.download_dir, file['title'])
                file.GetContentFile(file_path)
                self.logger.info(f"✅ Downloaded {file['title']} to {file_path}")
                print(f"✅ Downloaded {file['title']} to {file_path}")

    def extract_folder_id(self, url):
        if "folders/" in url:
            return url.split("folders/")[1].split("?")[0]
        return None
