import concurrent
import time
from concurrent import futures
from pathlib import Path

from jira import JIRA
from selenium import webdriver
import json

class BrowserWrapper:


    def __init__(self):
        self._driver = None
        config_path  = Path(__file__).resolve().parents[2].joinpath("config.json")
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        self.hub_url = self.config["hub_url"]
        self.url = self.config["url"]
        self.cookies = self.config["user_cookies"]
        print("Test Start")

    def create_options(self, browser_type):
        if browser_type == 'Chrome':
            options = webdriver.ChromeOptions()
        elif browser_type == 'Firefox':
            options = webdriver.FirefoxOptions()
        elif browser_type == 'Edge':
            options = webdriver.EdgeOptions()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        return options
    def get_driver(self,browser_name):
        if self.config["grid"]:
            options = self.set_up_capabilities(browser_name)
            self._driver = webdriver.Remote(command_executor=self.hub_url, options=options)
        else:
            options = self.create_options(browser_name)
            if browser_name == 'Chrome':
                self._driver = webdriver.Chrome(options=options)
            elif browser_name == 'Firefox':
                self._driver = webdriver.Firefox(options=options)
            elif browser_name == 'Edge':
                self._driver = webdriver.Edge(options=options)
        self._driver.get(self.url)
        self._driver.maximize_window()
        return self._driver

    def set_up_capabilities(self, browser_type):
        options = None
        if browser_type == 'Chrome':
            options = webdriver.ChromeOptions()
        elif browser_type == 'Firefox':
            options = webdriver.FirefoxOptions()
        elif browser_type == 'Edge':
            options = webdriver.EdgeOptions()
        #options.add_argument("--headless")
        return options

    def create_local_driver(self, browser_name):
        browser_name_lower = browser_name.lower()
        if browser_name_lower == 'Chrome':
            return webdriver.Chrome()
        elif browser_name_lower == 'Firefox':
            return webdriver.Firefox()
        elif browser_name_lower == 'Edge':
            return webdriver.Edge()
        else:
            raise ValueError("Browser type not supported")

    def run_single_browser(self):
        browser = self.config["browser"]
        if browser == "Chrome":
            self._driver = webdriver.Chrome()
        elif browser == "FireFox":
            self._driver = webdriver.Firefox()
        elif browser == "Edge":
            self._driver = webdriver.Edge()
        self._driver.get(self.url)
        self._driver.maximize_window()


    def build_cap(self):
        # proxy_ip = 'localhost'  # Default ZAP Proxy IP
        # proxy_port = '8081'  # Default ZAP Proxy Port
        # zap_proxy = f"{proxy_ip}:{proxy_port}"

        # self.chrome_cap.add_argument(f'--proxy-server={zap_proxy}')
        # self.chrome_cap.add_argument('--ignore-certificate-errors')

        self.firfox_cap = webdriver.FirefoxOptions()
        self.firfox_cap.capabilities['platformName'] = 'Windows'
        self.chrome_cap = webdriver.ChromeOptions()
        self.chrome_cap.capabilities['platformName'] = 'Windows'

        self.edge_cap = webdriver.EdgeOptions()
        self.edge_cap.capabilities['platformName'] = 'Windows'
        self.caps_list = [self.chrome_cap, self.edge_cap, self.firfox_cap]

    def teardown(self):
        self._driver.close()
        self._driver.quit()