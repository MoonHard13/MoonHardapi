import os
import json
import logging
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import zipfile
import re
import glob
import shutil

class ProgramDownloader:
    def __init__(self):
        self.download_links = {
            "Amvrosia Service": {
                "link": "https://drive.google.com/drive/folders/1LFaI84SbgPdTAGfkN1VKi8znqShpG_VV?usp=sharing",
                "pattern": "AmvrosiaService *.*.*"
            },
            "SnService": {
                "link": "https://drive.google.com/drive/folders/1zh10RewQXVAVsqFshpy8Kd6s8v88czfQ?usp=sharing",
                "pattern": "SnService *.*.*"
            },
            "CallServer Host": {
                "link": "https://drive.google.com/drive/folders/19o044imDR6DlHeY3h_7zcMUx8kSSE6N4?usp=sharing",
                "pattern": "CallServer Host *.*.*.*.msi"
            },
            "CallServer Client": {
                "link": "https://drive.google.com/drive/folders/1T3tQs4xdY1Ld0yvAuJVCvTirKJtlLdhM?usp=sharing",
                "pattern": "CallServer Client *.*.*.*.msi"
            },
            "External Provider": {
                "link": "https://drive.google.com/drive/folders/1tb477TDcTyufjab3VbSpu1l1Qfa60MJI?usp=sharing",
                "pattern": "Provider *.*.*.*"
            },
            "FnB Services": {
                "link": "https://drive.google.com/drive/folders/10nQSyoHzR45kyYhwLGWfMPRtvD4WBQaa?usp=sharing",
                "pattern": "FnB Services-*.*.*.*"
            },
            "AMVPMS": {
                "link": "https://drive.google.com/drive/folders/1Vn6zgrrxD-3KbPYKnKe-4-Ui5VCktrhM?usp=sharing",
                "pattern": "AMVPMS *.*.*"
            },
            "WebHookAPI": {
                "link": "https://drive.google.com/drive/folders/1T8O6xjke_5VLz7TfiiqyLMoRx9-QvFns?usp=sharing",
                "pattern": "WebHookAPI *.*.*.*"
            },
            "External Con API": {
                "link": "https://drive.google.com/drive/folders/1_kHDaukj4E0GwRCJY2tXmhqAFMO-V4_l?usp=sharing",
                "pattern": "External Connection Web API *.*.*.*"
            },
            "Main Apps": {
                "link": "https://drive.google.com/drive/folders/18I6QjSLxpXanFIvQwI5_3bXSX3ohBj6D?usp=sharing",
                "pattern": "Amvrosia Setup v.*.*.*.exe, BackOffice Setup v.*.*.*.exe"
            },
            "Statistics": {
                "link": "https://drive.google.com/drive/folders/14VNTSiHMql9EcOyoO_71kM29iCbFytmi?usp=sharing",
                "pattern": "Statistics *.*.*"
            },
            "Samtec": {
                "link": "https://drive.google.com/drive/folders/1ZqbwrULhAOKsUmbnVzJrk_U2UOirDZ0C?usp=sharing",
                "pattern": "Samtec"
            },
            "Copy S1DC": {
                "link": "https://drive.google.com/drive/folders/1SV7WVJka1Ux9Cz1NracRmPqXIR-Lnh7S?usp=sharing",
                "pattern": "s1dc"
            }
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
            os.system(f'attrib -R -S -H "{self.download_dir}"')
            os.system(f'net share SunsoftSetups="{self.download_dir}" /GRANT:Everyone,FULL')
            
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            
        client_secrets_path = os.path.join(self.base_dir, "client_secrets.json")
        if not os.path.exists(client_secrets_path):
            with open(client_secrets_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "installed": {
                        "client_id": "1095484660040-59otujsocc2ea86e6gph733okmofig8g.apps.googleusercontent.com",
                        "project_id": "sunsoft-downloader",
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "client_secret": "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",
                        "redirect_uris": ["http://localhost"]
                    }
                }, f, indent=2)

        creds_path = os.path.join(self.base_dir, "mycreds.txt")

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
        from pydrive2.auth import GoogleAuth
        from pydrive2.drive import GoogleDrive

        creds_path = os.path.join(self.base_dir, "mycreds.txt")
        client_secrets_path = os.path.join(self.base_dir, "client_secrets.json")

        gauth = GoogleAuth()
        gauth.LoadClientConfigFile(client_secrets_path)

        if not os.path.exists(creds_path):
            print("🔐 First-time auth: opening browser...")
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile(creds_path)
            return GoogleDrive(gauth)

        gauth.LoadCredentialsFile(creds_path)

        try:
            if gauth.access_token_expired or gauth.credentials is None:
                print("🔄 Access token expired or missing. Attempting silent refresh...")
                gauth.Refresh()
                gauth.SaveCredentialsFile(creds_path)
                print("✅ Token refreshed successfully.")
            else:
                gauth.Authorize()
        except Exception as e:
            print(f"❌ Silent token refresh failed: {e}")
            print("🌐 Re-authenticating via browser...")
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile(creds_path)

        return GoogleDrive(gauth)

    def download_programs(self, program_list):
        print("🚀 download_programs called with:", program_list)
        for program in program_list:
            entry = self.download_links.get(program)
            if not entry:
                msg = f"⚠️ Unknown program: {program}"
                print(msg)
                self.logger.warning(msg)
                continue

            # ✅ Delete previous versions first
            link = entry["link"]
            pattern = entry["pattern"]
            self.cleanup_existing_versions(pattern)
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
                # === Check and unzip if .zip ===
                if file_path.lower().endswith('.zip'):
                    extract_to = self.download_dir
                    os.makedirs(extract_to, exist_ok=True)
                    self.unzip_file(file_path, extract_to)

                self.logger.info(f"✅ Downloaded {file['title']} to {file_path}")
                print(f"✅ Downloaded {file['title']} to {file_path}")

    def extract_folder_id(self, url):
        if "folders/" in url:
            return url.split("folders/")[1].split("?")[0]
        return None

    def unzip_file(self, zip_path, extract_to):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            self.logger.info(f"📦 Extracted {zip_path} to {extract_to}")
            print(f"📦 Extracted {zip_path} to {extract_to}")

            # ✅ Delete the original zip
            os.remove(zip_path)
            self.logger.info(f"🗑️ Deleted zip file: {zip_path}")
            print(f"🗑️ Deleted zip file: {zip_path}")

        except Exception as e:
            self.logger.error(f"❌ Failed to unzip {zip_path}: {e}")
            print(f"❌ Failed to unzip {zip_path}: {e}")
            
    def cleanup_existing_versions(self, pattern_str):
        print(f"\n🧹 [CLEANUP] Using pattern: {pattern_str}")
        print(f"📁 Current contents of {self.download_dir}:")

        for entry in os.listdir(self.download_dir):
            print(f"  - {entry}")

        patterns = pattern_str.split(", ")
        for pattern in patterns:
            full_pattern = os.path.join(self.download_dir, pattern)
            print(f"🔍 Searching with glob: {full_pattern}")
            files = glob.glob(full_pattern)

            if not files:
                print("⚠️ No matches found for cleanup.")
            else:
                print(f"🔎 Matches found: {files}")

            for file in files:
                try:
                    if os.path.isfile(file):
                        os.remove(file)
                        print(f"🗑️ Deleted file: {file}")
                    elif os.path.isdir(file):
                        shutil.rmtree(file)
                        print(f"🗑️ Deleted folder: {file}")
                    self.logger.info(f"🗑️ Διεγράφη: {file}")
                except Exception as e:
                    print(f"❌ Failed to delete {file}: {e}")
                    self.logger.error(f"[Σφάλμα] Διαγραφής {file}: {e}")