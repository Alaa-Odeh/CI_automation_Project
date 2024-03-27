import json
from pathlib import Path

from jira import JIRA
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JiraWrapper:
    def __init__(self):
        config_path = Path(__file__).resolve().parents[2].joinpath("config_jira.json")
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        load_dotenv()
        TOKEN = os.getenv("JIRA_TOKEN")
        JIRA_USER = self.config["jira_user"]
        jira_url = self.config["jira_server"]
        self.auth_jira = JIRA(basic_auth=(JIRA_USER, TOKEN), options={"server": jira_url})

    def create_issue(self, summery, description, project_key='FAP',assignee='alaa odeh', issue_type="Bug"):
        issue_dict = {
            'project': {'key': project_key},
            'summary': f'failed test: {summery}',
            'description': description,
            'issuetype': {'name': issue_type},
            'assignee': assignee
        }
        new_issue = self.auth_jira.create_issue(fields=issue_dict)
        return new_issue.key