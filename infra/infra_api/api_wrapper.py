import json
from pathlib import Path

import requests
from jira import JIRA


class APIWrapper():
    def __init__(self):
        self.response=None
        self.my_request=requests
        config_path  = Path(__file__).resolve().parents[2].joinpath("config_api.json")

        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        self.token=self.config['token']
        self.url=self.config['url']

    def api_get_request(self,url):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        self.response=self.my_request.get(url, headers=headers)
        if self.response.ok:
            return self.response
        else:
            return self.response.status_code

    def api_post_request(self,url,body):

        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        self.response=self.my_request.post(url,json=body,headers=headers)
        if self.response.ok:
            return self.response
        else:
            return self.response.status_code

    def api_delete_request(self, url):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        self.response = self.my_request.delete(url, headers=headers)
        if self.response.ok:
            return self.response
        else:
            return self.response.status_code

    def api_put_request(self, url,body):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        self.response = self.my_request.put(url,json=body, headers=headers)
        if self.response.ok:
            return self.response
        else:
            return self.response.status_code

