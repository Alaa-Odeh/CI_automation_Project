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
        self.url = self.config["news"]
        token = 'ATATT3xFfGF09zxxyNEWZufXBZbGVJog8nRzG7_IggWzimhiYh0ZbFTfvsYNHfuCe_c1A_th5eeCINDMAvtgOWgGxLMtsNChMb-DRin7X8ip-sQxFFfuPJC-kvvwfuHeV2VATrvBPINg07GBKs9IkzwX20JpJLwKnF3uu-7tT3zIHqDo4qpyc6E=0C5BD39D'
        self.auth_jira = JIRA(basic_auth=("kharbosh.computer@gmail.com", token),
                         options={'server': self.config['jira_url']})
        self.project_key=self.config['project_key']
        self.token=self.config['token']
    def create_issue(self,summary,description,project_key,assignee='alaa odeh',issue_type='Bug'):
        issue_dict={
            'summary': summary,
            'description': description,
            'project':{'key': project_key},
            'issuetype': {'name':issue_type},
            'assignee': assignee}
        new_issue = self.auth_jira.create_issue(fields=issue_dict)
        return new_issue.key

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

