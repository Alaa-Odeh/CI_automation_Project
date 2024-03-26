from selenium.webdriver.common.by import By

class WelcomePage:
    LOG_IN_BUTTON='//a[@class="user-anonymous tnb-login-btn w3-bar-item w3-btn bar-item-hover w3-right ws-light-green ga-top ga-top-login"]'
    UPPER_FRAME='//iframe[@id="top-nav-bar-iframe"]'
    MY_PATH='//a[contains(text(),"My W3Schools")]'

    def __init__(self, driver):
        self._driver =driver
        self.my_path_button=self._driver.find_element(By.XPATH, self.MY_PATH)
    def init(self):
        self.log_in_button=self._driver.find_element(By.XPATH, self.LOG_IN_BUTTON)
        self.my_path_button=self._driver.find_element(By.XPATH, self.MY_PATH)

    def click_log_in(self):
        self.init()
        self.log_in_button.click()

    def click_My_Path(self):
        self.init()
        self.my_path_button.click()
