import time
import unittest

from infra.infra_web.browser_wrapper import BrowserWrapper
from logic.api_logic.goals_api import GoalsAPI
from logic.api_logic.skills_api import SkillsAPI
from logic.web_logic.goals_web import GoalsWeb
from logic.web_logic.home_page_pathfinder import PathfinderPage
from logic.web_logic.login_page import LoginPage
from logic.web_logic.welcome_page import WelcomePage


class TestGoalsAPI(unittest.TestCase):
    def setUp(self):
        self.goals_api = GoalsAPI()
        self.skills = SkillsAPI()
        #self.browser = BrowserWrapper()

        #self.driver = self.browser._driver

        self.welcome_page = WelcomePage(self.driver)
        self.welcome_page.click_log_in()
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow("friendola15@gmail.com", "AutomationTester2024")
        self.pathfinder_page = PathfinderPage(self.driver)
        self.pathfinder_page.click_on_Goals_page()
        self.goals_web = GoalsWeb(self.driver)

    def test_create_goal_api(self):
        self.goal_name="Frontend developer"
        chosen_skills=["C#","Java","Python","Go"]
        courses_levels=["Professional","Beginner","Professional","Beginner"]
        hours_weekly=8

        self.goals_web.set_goal_in_web(self.goal_name,chosen_skills,courses_levels,hours_weekly)
        skill_names,skill_levels,hours_per_week= self.goals_api.get_goal_info(chosen_skills)


        self.assertListEqual(skill_names,chosen_skills,"Skills dont match")
        self.assertListEqual(skill_levels,courses_levels,"levels Dont Match")
        self.assertEqual(hours_per_week,hours_weekly,"Weekly hours Dont match")
    def tearDown(self):
        self.driver.refresh()
        self.goals_web.delete_goals(self.goal_name)


