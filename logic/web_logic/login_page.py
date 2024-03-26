import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage():
    CONTINUE_WITH_GOOGLE="//div[contains(text(),'Continue with Google')]"
    EMAIL_INPUT = '//input[@autocomplete="username"]'
    NEXT_BUTTON='//button[./span[contains(text(),"Next")]]'
    PASSWORD_INPUT='//input[@autocomplete="current-password"]'
    PASSWORD_NEXT_BUTTON='//button[./span[contains(text(),"Next")]]'
    LOG_IN_BUTTON='//button[@class="Button_button__URNp+ Button_primary__d2Jt3 Button_fullwidth__0HLEu"]'
    WRONG_PASSWORD="//div[@jsname='B34EJ']"


    def __init__(self, driver):
        self._driver =driver
        self._driver.implicitly_wait(5)

    def init(self):
        self.continue_with_google = WebDriverWait(self._driver,20).until(EC.presence_of_element_located((By.XPATH, self.CONTINUE_WITH_GOOGLE)))
        self.log_in_button = self._driver.find_element(By.XPATH, self.LOG_IN_BUTTON)

    def click_continue_with_google_button(self):
        self.init()
        self.continue_with_google.click()

    def fill_email_input_field(self,email):
        self.email_input = self._driver.find_element(By.XPATH, self.EMAIL_INPUT)
        self.email_input.send_keys(email)
    def click_next_button(self,element):
        time.sleep(3)
        self.next_button = WebDriverWait(self._driver,30).until(EC.presence_of_element_located((By.XPATH, element))).click()

    def fill_password_input_field(self,password):
        self.password_input=WebDriverWait(self._driver,30).until(EC.visibility_of_element_located((By.XPATH,self.PASSWORD_INPUT)))
        self.password_input.send_keys(password)


    def login_flow(self,email,password):
        self.click_continue_with_google_button()
        self.fill_email_input_field(email)
        self.click_next_button(self.NEXT_BUTTON)
        self.fill_password_input_field(password)
        self.click_next_button(self.PASSWORD_NEXT_BUTTON)

    def login_with_invalid_password(self,email,password):
        self.login_flow( email, password)
        self.wrong_password_message = WebDriverWait(self._driver,15).until(EC.visibility_of_element_located((By.XPATH,self.WRONG_PASSWORD)))
        return self.wrong_password_message.text







