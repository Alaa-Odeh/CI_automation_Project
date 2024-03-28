import datetime
import json
import unittest
from pathlib import Path
from ddt import ddt, data, unpack
from infra.infra_web.jira_wrapper import JiraWrapper
from logic.api_logic.goals_api import GoalsAPI

def load_test_data(filename):
    # Get the absolute path to the root directory of the project
    project_root = Path(__file__).resolve().parents[2]
    # Construct the path to the data file, assuming 'data' directory is at the project root
    data_file = project_root / 'data' / filename
    with open(data_file, 'r') as file:
        return json.load(file)

# Usage
test_data = load_test_data('test_data.json')
@ddt
class TestGoalsAPIGenerate(unittest.TestCase):

    def setUp(self):
        self.goals_api = GoalsAPI()
        self.jira_client = JiraWrapper()
        self.test_failed = False
    @data(*test_data)

    @unpack
    def test_generate_api_test(self, goal_name, skills, levels, hours_per_week):
        self.goals_api.post_new_goal(goal_name, skills, levels, hours_per_week)
        skill_names, skill_levels, updated_hours_per_week = self.goals_api.get_goal_info(goal_name)
        try:
            self.assertListEqual( sorted(skill_names) , sorted(skills), "Skills do not match")
            self.assertListEqual( sorted(skill_levels) , sorted(levels), "Levels do not match")
            self.assertEqual( updated_hours_per_week , hours_per_week, "Weekly hours not updated")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise


    def tearDown(self):
        self.goals_api.delete_goal()
        self.test_name = self.id().split('.')[-1]
        if self.test_failed:
            self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            summary = f"Test failed: {self.test_name} generated an error at {self.current_time}"
            description = f"{self.error_msg}"
            try:
                issue_key = self.jira_client.create_issue(summary, description)
                print(f"Jira issue created: {issue_key}")
            except Exception as e:
                print(f"Failed to create Jira issue: {e}")
