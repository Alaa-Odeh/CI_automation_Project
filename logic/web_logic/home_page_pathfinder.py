import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logic.web_logic.svg_tutorial import SvgTutorial


class PathfinderPage(object):
    MY_W3SCHOOLS_LOGGED_IN='//h2[@class="chakra-heading css-wnbja6"]'
    GOALS_LINK= '//a[./p[contains(text(),"Goals")]]'
    TESTS_LINK='//a[./p[contains(text(),"Tests")]]'
    SKILLS_LINK='//a[./p[contains(text(),"Skills")]]'
    TOGGLE_BUTTON='//*[@class="chakra-button css-1lfqljy"]'
    TUTORIALS_BUTTON='//a[@id="navbtn_tutorials"]'
    LEARN_SVG='//a[@class="w3-bar-item w3-button acctop-link ga-top-drop ga-top-drop-tut-svg"]'
    UPPER_FRAME='//iframe[@id="top-nav-bar-iframe"]'


    def __init__(self, driver):
        self._driver =driver
        wait = WebDriverWait(driver, 20)  # Timeout of 10 seconds

    def init(self):
        self.goals_button=WebDriverWait(self._driver,15).until(EC.visibility_of_element_located((By.XPATH, self.GOALS_LINK)))
        self.tests_button=WebDriverWait(self._driver,20).until(EC.visibility_of_element_located((By.XPATH, self.TESTS_LINK)))
        self.light_mode_button=WebDriverWait(self._driver,15).until(EC.element_to_be_clickable((By.XPATH, self.TOGGLE_BUTTON)))
        self.skills_button=WebDriverWait(self._driver,15).until(EC.visibility_of_element_located((By.XPATH, self.SKILLS_LINK)))


    def click_on_Goals_page(self):
        self.init()
        self.goals_button.click()
