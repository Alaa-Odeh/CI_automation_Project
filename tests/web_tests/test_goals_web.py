import time
import unittest
from infra.infra_web.browser_wrapper import BrowserWrapper
from logic.api_logic.goals_api import GoalsAPI
from logic.web_logic.goals_web import GoalsWeb
from logic.web_logic.home_page_pathfinder import PathfinderPage
from logic.web_logic.login_page import LoginPage
from logic.web_logic.welcome_page import WelcomePage


class TestGoalsWeb(unittest.TestCase):
    def setUp(self):
        self.goals_api=GoalsAPI()
        self.browser = BrowserWrapper()
        self.driver = self.browser._driver

        self.welcome_page = WelcomePage(self.driver)
        self.welcome_page.click_log_in()
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow("friendola15@gmail.com", "AutomationTester2024")
        self.pathfinder_page = PathfinderPage(self.driver)
        self.pathfinder_page.click_on_Goals_page()
        self.goals_web=GoalsWeb(self.driver)


    def test_create_goal_web(self):
        self.goal_name="Backend developer"
        skills=["HTML","C#","C++"]
        levels=["Professional","Advanced","Beginner"]
        hours_per_week=8

        sorted_skills,sorted_levels=self.goals_web.sort_skills_and_levels(skills, levels)

        self.goals_api.post_new_goal(self.goal_name,skills,levels,hours_per_week)
        self.driver.refresh()
        self.goals_web.extract_goal_skills_level(self.goal_name)

        self.assertEqual(self.goals_web.goal_name_in_my_goals.text,self.goal_name,"Goal name Does Not Exist in My Goals Page")
        self.assertListEqual(self.goals_web.skills_names, sorted_skills,"Missing a skill in the Goal")
        self.assertListEqual(self.goals_web.matching_level_names,sorted_levels,"Missing skill level")

    def tearDown(self):
        self.goals_web.delete_goals(self.goal_name)

