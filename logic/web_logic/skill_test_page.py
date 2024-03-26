from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from logic.web_logic.python_test_page import PythonTestPage


class SkillTestPage:

    CONTINUE_TEST_BUTTON='//button[@class="chakra-button css-1vq2iti"]'
    QUESTIONS_ANSWERED= '//p[@class="chakra-text css-82xjxz"]'
    TEST_HISTORY = '//p[@class="chakra-text css-1gqpmn1"]'
    NOT_COMPLETED_TEST='//div[@class="css-mvit9d"]//p[@class="chakra-text css-mcmk74"]'
    TEST_HISTORY_BUTTON='//button[@class="chakra-accordion__button css-uttm9k"]'
    DELETE_COMPLETED_TEST="//button[@class='css-wxbj87']"
    FINAL_DELETE_BUTTON="//button[normalize-space()='Delete']"
    def __init__(self,driver):
        self._driver =driver
        while True:
            try:
                self.continue_test_button=WebDriverWait(self._driver,10).until(EC.visibility_of_element_located((By.XPATH,self.CONTINUE_TEST_BUTTON)))
                break

            except:
                self._driver.execute_script("window.scrollBy(0, 350);")


        self.python_answer=PythonTestPage(self._driver)
        self.original_window=self._driver.current_window_handle

    def click_test_history_button(self):
        self.completed_test_button.click()
    def click_final_delete_button(self):
        self.final_delete_button.click()

    def click_delete_completed_test(self):
        self.delete_completed_test.click()

    def click_continue_test(self):
        self._driver.implicitly_wait(10)
        self.continue_test_button.click()

    def answer_test_questions(self,number_of_questions):
        self.click_continue_test()
        self._driver.switch_to.window(self._driver.window_handles[-1])
        self.python_answer.answer_number_of_questions_test_questions(number_of_questions)
        self._driver.switch_to.window(self.original_window)

    def get_number_of_questions_answered(self):
        self._driver.refresh()
        return WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH,self.QUESTIONS_ANSWERED))).text.split()[0]


    def answer_all_test_questions(self):
        self.not_completed_test=WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH,self.NOT_COMPLETED_TEST)))
        self.click_continue_test()
        self._driver.switch_to.window(self._driver.window_handles[-1])
        self.python_answer.answer_all_test_questions()
        self._driver.switch_to.window(self.original_window)
        return self.not_completed_test.text

    def get_test_history(self):
        self._driver.refresh()
        self.test_history=WebDriverWait(self._driver, 15).until(EC.visibility_of_element_located((By.XPATH,self.TEST_HISTORY)))
        return self.test_history.text




