import unittest

from infra.infra_web.browser_wrapper import BrowserWrapper
from logic.api_logic.goals_api import GoalsAPI
from logic.web_logic.goals_web import GoalsWeb
from logic.web_logic.home_page_pathfinder import PathfinderPage
from logic.web_logic.login_page import LoginPage
from logic.web_logic.welcome_page import WelcomePage


class TestUpdateGoalAPI(unittest.TestCase):
    def setUp(self):
        self.goals_api = GoalsAPI()
        self.browser = BrowserWrapper()
        if self.browser.config["grid"]:
            self.browser.build_cap()
        else:
            self.browser.run_single_browser()
        self.driver = self.browser._driver
        self.welcome_page = WelcomePage(self.driver)
        self.welcome_page.click_log_in()
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow("friendola15@gmail.com", "AutomationTester2024")
        self.pathfinder_page = PathfinderPage(self.driver)
        self.pathfinder_page.click_on_Goals_page()
        self.goals_web = GoalsWeb(self.driver)
        self.goal_name = "Backend developer"
        self.chosen_skills = ["HTML", "C#", "CSS"]
        self.courses_levels = ["Professional", "Beginner", "Beginner"]
        self.hours_weekly = 8
        self.goals_web.set_goal_in_web(self.goal_name, self.chosen_skills, self.courses_levels, self.hours_weekly)


    def test_update_goal_api(self):
        chosen_skills_to_update=["Go"]
        courses_levels_to_update=["Intermediate"]
        hours_weekly = 16

        self.goals_web.make_changes(self.goal_name,chosen_skills_to_update,courses_levels_to_update,hours_weekly)

        skill_names,skill_levels,hours_per_week= self.goals_api.get_goal_info(chosen_skills_to_update+self.chosen_skills)

        self.assertListEqual(skill_names, chosen_skills_to_update+self.chosen_skills, "Skills dont match")
        self.assertListEqual(skill_levels, courses_levels_to_update+self.courses_levels, "levels Dont Match")
        self.assertEqual(hours_per_week, hours_weekly, "Weekly hours not updated")

    def tearDown(self):
        self.goals_api.delete_goal()