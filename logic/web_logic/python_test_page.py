import re

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random




class PythonTestPage:
    RESUME_TEST_BUTTON='//button[contains(text(),"Resume")]'
    NEXT_QUESTION_BUTTON='//button[contains(text(),"Next Question")]'
    ANSWERS_LABEL='//label[@class="css-pzgccd"]'
    PROGRESS_BAR='//div[@class="css-as8crt"]'
    CLOSE_TEST_BUTTON='//button[contains(text(),"Close")]'


    def __init__(self, driver):
        self._driver =driver


    def init(self):
        self.resume_test_button=WebDriverWait(self._driver, 60).until(EC.visibility_of_element_located((By.XPATH, self.RESUME_TEST_BUTTON)))

    def click_resume_test_button(self):
        self.init()
        self.resume_test_button.click()

    def get_question_options(self):
        self.options = WebDriverWait(self._driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,self.ANSWERS_LABEL )))

    def choose_random_answer(self):
        random_choice = random.choice(self.options)
        random_choice.click()
        while True:
            try:
                self.next_question_button = WebDriverWait(self._driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.NEXT_QUESTION_BUTTON)))
                break
            except:
                self._driver.execute_script("window.scrollBy(0, 350);")


    def click_next_question_button(self):
        self.next_question_button.click()

    def answer_one_question_randomly(self):

        self.get_question_options()
        self.choose_random_answer()
        self.click_next_question_button()

    def answer_number_of_questions_test_questions(self,number_of_questions):
        self.click_resume_test_button()
        for i in range(number_of_questions):
            self.answer_one_question_randomly()
        self._driver.close()


    def answer_all_test_questions(self):
        self.click_resume_test_button()
        while True:
            try:  # If the element is visible, exit the loop
                self.answer_one_question_randomly()
            except:
                element = self._driver.find_element(By.XPATH, self.CLOSE_TEST_BUTTON)
                element.click()
                break
