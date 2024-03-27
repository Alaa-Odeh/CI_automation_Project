import json
import unittest
from pathlib import Path

from ddt import ddt, data, unpack
from logic.api_logic.goals_api import GoalsAPI
from pytest_markers import test_decorator

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
    @data(*test_data)

    @unpack
    def test_generate_api_test(self, goal_name, skills, levels, hours_per_week):
        self.goals_api.post_new_goal(goal_name, skills, levels, hours_per_week)
        skill_names, skill_levels, updated_hours_per_week = self.goals_api.get_goal_info(goal_name)

        self.assertListEqual( sorted(skill_names) , sorted(skills), "Skills do not match")
        self.assertListEqual( sorted(skill_levels) , sorted(levels), "Levels do not match")
        self.assertEqual( updated_hours_per_week , hours_per_week, "Weekly hours not updated")


    def tearDown(self):
        self.goals_api.delete_goal()  # Use the stored goal name to delete the goal
