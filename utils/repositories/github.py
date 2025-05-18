import requests
import configparser

from core.settings import config_file

class github():

    def __init__(self):
        self.base_url = "https://api.github.com"

        self.parser = configparser.ConfigParser()
        self.parser.read(config_file)
        self.token = self.parser['github']['token']

        #self.token = config_file.get("github", "token")

        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def create_repo(self, repo_name: str, description: str = "", private: bool = True):
        url = f"{self.base_url}/user/repos"

        payload = {
            "name": repo_name,
            "description": description,
            "private": private
        }
        
        return requests.post(url, json=payload, headers=self.headers)
    