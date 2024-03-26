import time
import unittest

from infra.infra_web.browser_wrapper import BrowserWrapper
from logic.api_logic.goals_api import GoalsAPI
from logic.web_logic.goals_web import GoalsWeb
from logic.web_logic.home_page_pathfinder import PathfinderPage
from logic.web_logic.login_page import LoginPage
from logic.web_logic.welcome_page import WelcomePage


class TestDeleteGoalWeb(unittest.TestCase):
    def setUp(self):
        self.goals_api = GoalsAPI()
        #self.browser = BrowserWrapper()
        #if self.browser.config["grid"]:
        #    self.browser.build_cap()
        #else:
        #    self.browser.run_single_browser()
        #self.driver = self.browser._driver
        self.welcome_page = WelcomePage(self.driver)
        self.welcome_page.click_log_in()
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow("friendola15@gmail.com", "AutomationTester2024")
        self.pathfinder_page = PathfinderPage(self.driver)
        self.pathfinder_page.click_on_Goals_page()
        self.goals_web = GoalsWeb(self.driver)
        self.goal_name = "Game developer"
        skills = ["HTML", "C#", "C++", "JavaScript", "DSA"]
        levels = ["Professional", "Advanced", "Intermediate", "Beginner", "Professional"]
        hours_per_week = 10
        self.goals_api.post_new_goal(self.goal_name, skills, levels, hours_per_week)

    def test_delete_goal(self):
        self.goals_api.delete_goal()
        self.driver.refresh()
        self.goals_web.extract_goal_skills_level(self.goal_name)
        self.assertEqual(self.goals_web.goal_name_in_my_goals,f"Goal name '{self.goal_name}' was not found on the page.","Goal was Not Deleted")

    #def tearDown(self):
     #   self.goals_api.delete_goal()