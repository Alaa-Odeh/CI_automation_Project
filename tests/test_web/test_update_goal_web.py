import json
import time
import unittest
from pathlib import Path

from parameterized import parameterized_class

from infra.infra_web.browser_wrapper import BrowserWrapper
from logic.api_logic.goals_api import GoalsAPI
from logic.web_logic.goals_web import GoalsWeb
from logic.web_logic.home_page_pathfinder import PathfinderPage
from logic.web_logic.login_page import LoginPage
from logic.web_logic.welcome_page import WelcomePage
from pytest_markers import test_decorator

config_path = Path(__file__).resolve().parents[2].joinpath("config.json")
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
browser_types = [(browser,) for browser in config["browser_types"]]
@parameterized_class(('browser',), browser_types)
class TestUpdateGoalWeb(unittest.TestCase):
    def setUp(self):
        self.goals_api=GoalsAPI()
        self.browser_wrapper = BrowserWrapper()
        default_browser = 'Chrome'
        self.browser = getattr(self.__class__, 'browser', default_browser)
        self.driver = self.browser_wrapper.get_driver(browser_name=self.browser)
        self.welcome_page = WelcomePage(self.driver)
        self.welcome_page.click_log_in()
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow("friendola15@gmail.com", "AutomationTester2024")
        self.pathfinder_page = PathfinderPage(self.driver)
        self.pathfinder_page.click_on_Goals_page()
        self.goals_web=GoalsWeb(self.driver)
        self.goal_name = "Game developer"
        skills = ["HTML", "C#","C++","JavaScript","DSA"]
        levels = ["Professional", "Advanced","Intermediate","Beginner","Professional"]
        hours_per_week = 10
        self.goals_api.post_new_goal(self.goal_name, skills, levels, hours_per_week)
    @test_decorator
    def test_update_goal_web(self):
        chosen_skills_to_update = ["Go","C++","JavaScript"]
        courses_levels_to_update = ["Intermediate","Beginner","Professional"]
        hours_weekly = 16
        self.goals_api.update_an_existing_goal(self.goal_name, chosen_skills_to_update,courses_levels_to_update,hours_weekly)
        self.driver.refresh()

        self.sorted_skills, self.sorted_levels = self.goals_web.sort_skills_and_levels(chosen_skills_to_update, courses_levels_to_update)
        self.goals_web.extract_goal_skills_level(self.goal_name)
        self.assertEqual(self.goals_web.goal_name_in_my_goals.text, self.goal_name,"Goal name Does Not Exist in My Goals Page")
        self.assertListEqual(self.goals_web.skills_names, self.sorted_skills, "Missing a skill in the Goal")
        self.assertListEqual(self.goals_web.matching_level_names, self.sorted_levels, " skill levels dont match")


    def tearDown(self):
        self.goals_api.delete_goal()

