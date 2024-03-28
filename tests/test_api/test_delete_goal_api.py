import datetime
import time
import unittest
from infra.infra_web.browser_wrapper import BrowserWrapper
from infra.infra_web.jira_wrapper import JiraWrapper
from logic.api_logic.goals_api import GoalsAPI
from logic.web_logic.goals_web import GoalsWeb
from logic.web_logic.home_page_pathfinder import PathfinderPage
from logic.web_logic.login_page import LoginPage
from logic.web_logic.welcome_page import WelcomePage



class TestDeleteGoalAPI(unittest.TestCase):
    default_browser = 'Chrome'
    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.browser_wrapper.run_single_browser()
        self.driver = self.browser_wrapper._driver
        self.jira_client=JiraWrapper()
        self.test_failed = False

        self.welcome_page = WelcomePage(self.driver)
        self.goals_api = GoalsAPI()
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
        time.sleep(1)
        goal_id_after_deleting=self.goals_api.get_goal_id()
        try:
            self.assertEqual(len(goal_id_before_deleting), 34, "Goal was not created")
            self.assertEqual(goal_id_after_deleting, None, "Goal was not Deleted")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def tearDown(self):
        self.goals_api.delete_goal()
        self.driver.close()
        self.driver.quit()
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

