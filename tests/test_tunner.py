import concurrent.futures
import datetime
import json
from pathlib import Path
import time
import unittest
import logging
from infra.infra_api.api_wrapper import APIWrapper
from infra.infra_web.browser_wrapper import BrowserWrapper
from tests.api_tests.test_delete_goal_api import TestDeleteGoalAPI
from tests.api_tests.test_goals_api import TestGoalsAPI
from tests.api_tests.test_update_goal_api import TestUpdateGoalAPI
from tests.web_tests.test_goals_web import TestGoalsWeb
from tests.web_tests.test_delete_goal_web import TestDeleteGoalWeb
from tests.web_tests.test_update_goal_web import TestUpdateGoalWeb


class ContinueTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.browser_wrapper = BrowserWrapper()
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

'''
    def addError(self, test, err):
        super().addError(test, err)
        # Log the error to Jira
        error_msg = self._exc_info_to_string(err, test)
        try:
            self.api_wrapper.create_issue(f"{test.id()} generated an error at {self.current_time}", error_msg, "FAP")
        except Exception as e:
            logging.error(f"Failed to create issue in Jira for error: {e}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        # Log the failure to Jira without calling the superclass method
        error_msg = str(err[1])
        self.api_wrapper.create_issue(f"{test.id()} failed at {self.current_time}", error_msg, "FAP")
'''

def run_individual_test(test,cap=None):
    browser_wrapper.get_driver(cap)
    test.browser=browser_wrapper
    test.driver=browser_wrapper._driver
    suite = unittest.TestSuite([test])
    runner = unittest.TextTestRunner(resultclass=ContinueTestResult)
    runner.run(suite)


if __name__ == '__main__':
    browser_wrapper = BrowserWrapper()
    start_time = time.time()

    #test_classes = [TestGoalsWeb,TestGoalsAPI,TestUpdateGoalAPI,TestUpdateGoalWeb,TestDeleteGoalAPI,TestDeleteGoalWeb]
    test_classes = [TestDeleteGoalAPI]

    all_test_cases = []
    for test_class in test_classes:
        test_suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        for test_case in test_suite:
            all_test_cases.append(test_case)

    cur_dir = Path(__file__).resolve().parents[1].joinpath("config.json")
    with open(cur_dir, 'r') as config_file:
        config = json.load(config_file)

    if config["grid"] :
        browser_wrapper.build_cap()
        if config["grid type"] == "parallel":
            with concurrent.futures.ThreadPoolExecutor(max_workers=config["grid size"]) as executor:

                for test in all_test_cases:
                    for cap in browser_wrapper.caps_list:
                        executor.submit(run_individual_test,test_case, cap)
                        time.sleep(10)
               # for future in concurrent.futures.as_completed(future_to_test):
                #    test = future_to_test[future]
                 #   try:
                  #      future.result()
                   # except Exception as e:
                    #    logging.error(f"Test execution or issue logging failed: {e}")
        elif config["grid type"] == "serial":
            for test  in all_test_cases:
                for cap in browser_wrapper.caps_list:
                    run_individual_test(test,cap)
                    time.sleep(3)
    else:
        for test in all_test_cases:
            run_individual_test(test)



    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time to run all tests: {total_time:.2f} seconds")
