import json
import time
import unittest
import datetime
from pathlib import Path

from parameterized import parameterized_class

from infra.infra_web.browser_wrapper import BrowserWrapper
from infra.infra_web.jira_wrapper import JiraWrapper
from logic.api_logic.goals_api import GoalsAPI
from logic.web_logic.goals_web import GoalsWeb
from logic.web_logic.home_page_pathfinder import PathfinderPage
from logic.web_logic.login_page import LoginPage
from logic.web_logic.welcome_page import WelcomePage

class TestUpdateGoalWeb(unittest.TestCase):
    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.browser_wrapper.run_single_browser()
        self.driver = self.browser_wrapper._driver
        self.jira_client = JiraWrapper()
        self.test_failed = False
        self.goals_api=GoalsAPI()
        self.jira_client = JiraWrapper()

        self.welcome_page = WelcomePage(self.driver)
        self.welcome_page.click_log_in()
        self.login_page = LoginPage(self.driver)
        self.login_page.login_flow("friendola15@gmail.com", "AutomationTester2024")
        self.pathfinder_page = PathfinderPage(self.driver)
        self.pathfinder_page.click_on_Goals_page()
        self.goals_web=GoalsWeb(self.driver)
        self.goal_name = "Game developer"
        self.skills = ["HTML", "C#","C++","Java","DSA"]
        self.levels = ["Professional", "Advanced","Intermediate","Beginner","Professional"]
        self.hours_per_week = 10
        self.goals_api.post_new_goal(self.goal_name, self.skills, self.levels, self.hours_per_week)

    def test_update_goal_web(self):
        chosen_skills_to_update = ["Go","JavaScript"]
        courses_levels_to_update = ["Intermediate","Beginner"]
        hours_weekly = 16

        self.goals_api.update_an_existing_goal(self.goal_name, chosen_skills_to_update,courses_levels_to_update,hours_weekly)
        self.driver.refresh()
        time.sleep(3)
        skills_names,matching_level_names=self.goals_web.extract_goal_skills_level(self.goal_name)

        try:
            self.assertEqual(self.goals_web.goal_name_in_my_goals.text, self.goal_name,"Goal name Does Not Exist in My Goals Page")
            self.assertListEqual(sorted(skills_names), sorted((chosen_skills_to_update)), "Missing a skill in the Goal")
            self.assertListEqual(sorted(matching_level_names), sorted(courses_levels_to_update), " skill levels dont match")
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

