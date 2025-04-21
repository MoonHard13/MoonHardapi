import requests

class DashboardController:
    def __init__(self, server_url, auth_token):
        self.server_url = server_url
        self.token = auth_token

    def broadcast_command(self, command):
        url = f"{self.server_url}/broadcast?token={self.token}&command={command}"
        try:
            response = requests.post(url)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_status(self):
        url = f"{self.server_url}/status"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def send_to_client(self, client_id, command):
        try:
            url = f"{self.server_url}/send/{client_id}?token={self.auth_token}&command={command}"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def rename_client(self, client_id, new_name):
        try:
            url = f"{self.server_url}/rename/{client_id}?token={self.auth_token}&name={new_name}"
            response = requests.post(url)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
