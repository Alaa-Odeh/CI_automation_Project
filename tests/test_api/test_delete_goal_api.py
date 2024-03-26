import time
import unittest

from infra.infra_web.browser_wrapper import BrowserWrapper
from logic.api_logic.goals_api import GoalsAPI
from logic.web_logic.goals_web import GoalsWeb
from logic.web_logic.home_page_pathfinder import PathfinderPage
from logic.web_logic.login_page import LoginPage
from logic.web_logic.welcome_page import WelcomePage


class TestDeleteGoalAPI(unittest.TestCase):
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
        self.goal_name = "Fullstack developer"
        self.chosen_skills = ["Go", "Java", "CSS"]
        self.courses_levels = ["Professional", "Beginner", "Beginner"]
        self.hours_weekly = 8
        self.goals_web.set_goal_in_web(self.goal_name, self.chosen_skills, self.courses_levels, self.hours_weekly)

    def test_delete_goal_api(self):
        goal_id_before_deleting=self.goals_api.get_goal_id()
        self.goals_web.delete_goals(self.goal_name)
        time.sleep(3)
        goal_id_after_deleting=self.goals_api.get_goal_id()
        self.assertEqual(len(goal_id_before_deleting), 36, "Goal was not created")
        self.assertEqual(goal_id_after_deleting, None, "Goal was not Deleted")

    def tearDown(self):
        self.goals_api.delete_goal()


