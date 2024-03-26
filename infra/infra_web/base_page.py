import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
class BasePage:
    def __init__(self,driver):
        self._driver =driver


    def get_header(self):
        return WebDriverWait(self._driver,20).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))


    def get_page_title(self):
        return self._driver.title

    def get_current_url(self):
        return self._driver.current_url()