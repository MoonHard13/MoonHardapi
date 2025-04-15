import os
import json
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
            os.system(f'attrib -R -S -H \"{self.download_dir}\"')
            os.system(f'net share SunsoftSetups="{self.download_dir}" /GRANT:Everyone,FULL')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        client_secrets_path = os.path.join(self.base_dir, "client_secrets.json")
        if not os.path.exists(client_secrets_path):
            with open(client_secrets_path, 'w', encoding='utf-8') as f:
                json.dump({"udl_path": "C:/ProgramData/Sunsoft/Back Office/Initial.udl"}, f, indent=2)

        creds_path = os.path.join(self.base_dir, "mycreds.txt")
        if not os.path.exists(creds_path):
            with open(creds_path, 'w', encoding='utf-8') as f:
                f.write('{"access_token": "ya29.a0AZYkNZhyy0os_8qdE-TMrpUx71MdH8Mp_YYHO7nN76LgVyWLy5-Va079uR4m8M0cSM8TUhl3ac9PDmTHY1fv3fML6NDD9aaaqmTizh4ajuFIoeTU9QdXSDoqWxMUsQvkkg_XSM2UeIHltcbOJBp1Y-s7xXetTNHU_rS1iVuxaCgYKARwSARISFQHGX2MiXf0kE6N72bgLAjjEfcPGfQ0175", "client_id": "1095484660040-59otujsocc2ea86e6gph733okmofig8g.apps.googleusercontent.com", "client_secret": "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", "refresh_token": "1//09tJDoXRsfc_aCgYIARAAGAkSNwF-L9IrFH44Pjm1cshO3wu1zN83AXcIiKC096f51iyGPJuyLpJE4HjyO9ZKOArD5Kwx9dUVGwE", "token_expiry": "2025-04-14T12:44:36Z", "token_uri": "https://oauth2.googleapis.com/token", "user_agent": null, "revoke_uri": "https://oauth2.googleapis.com/revoke", "id_token": null, "id_token_jwt": null, "token_response": {"access_token": "ya29.a0AZYkNZhyy0os_8qdE-TMrpUx71MdH8Mp_YYHO7nN76LgVyWLy5-Va079uR4m8M0cSM8TUhl3ac9PDmTHY1fv3fML6NDD9aaaqmTizh4ajuFIoeTU9QdXSDoqWxMUsQvkkg_XSM2UeIHltcbOJBp1Y-s7xXetTNHU_rS1iVuxaCgYKARwSARISFQHGX2MiXf0kE6N72bgLAjjEfcPGfQ0175", "expires_in": 3599, "refresh_token": "1//09tJDoXRsfc_aCgYIARAAGAkSNwF-L9IrFH44Pjm1cshO3wu1nN83AXcIiKC096f51iyGPJuyLpJE4HjyO9ZKOArD5Kwx9dUVGwE", "scope": "https://www.googleapis.com/auth/drive", "token_type": "Bearer", "refresh_token_expires_in": 604799}, "scopes": ["https://www.googleapis.com/auth/drive"], "token_info_uri": "https://oauth2.googleapis.com/tokeninfo", "invalid": false, "_class": "OAuth2Credentials", "_module": "oauth2client.client"}')

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
