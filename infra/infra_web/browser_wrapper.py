import concurrent
import time
from concurrent import futures
from pathlib import Path

from jira import JIRA
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import json

class BrowserWrapper:


    def __init__(self):
        self._driver = None
        config_path  = Path(__file__).resolve().parents[2].joinpath("config.json")
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        self.hub_url = self.config["hub_url"]
        self.cookies = self.config["user_cookies"]


        token = 'ATATT3xFfGF09zxxyNEWZufXBZbGVJog8nRzG7_IggWzimhiYh0ZbFTfvsYNHfuCe_c1A_th5eeCINDMAvtgOWgGxLMtsNChMb-DRin7X8ip-sQxFFfuPJC-kvvwfuHeV2VATrvBPINg07GBKs9IkzwX20JpJLwKnF3uu-7tT3zIHqDo4qpyc6E=0C5BD39D'
        auth_jira = JIRA(basic_auth=("kharbosh.computer @ gmail.com", token), options={'server': self.config['jira_url']})
        print("Test Start")



    def get_driver(self,caps=None,user=None):

        if self.config["grid"]:
                self._driver = webdriver.Remote(command_executor=self.hub_url, options=caps)
        else:
            self.run_single_browser()
        self._driver.get(self.config["url"])
        self._driver.maximize_window()

    def build_cap(self):
        #proxy_ip = 'localhost'  # Default ZAP Proxy IP
        #proxy_port = '8081'  # Default ZAP Proxy Port
        #zap_proxy = f"{proxy_ip}:{proxy_port}"

        #self.chrome_cap.add_argument(f'--proxy-server={zap_proxy}')
        #self.chrome_cap.add_argument('--ignore-certificate-errors')

        self.firfox_cap=webdriver.FirefoxOptions()
        self.firfox_cap.capabilities['platformName'] = 'Windows'
        self.chrome_cap = webdriver.ChromeOptions()
        self.chrome_cap.capabilities['platformName'] = 'Windows'

        self.edge_cap = webdriver.EdgeOptions()
        self.edge_cap.capabilities['platformName'] = 'Windows'
        self.caps_list = [self.chrome_cap,self.edge_cap,self.firfox_cap]

    def test_grid_parallel(self,test_cases,user=None):
        self.test_cases=test_cases
        self.user=user
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.caps_list)) as executor:

            for test_case, cap in [(test_case, cap) for test_case in self.test_cases for cap in self.caps_list]:
                 executor.submit(self.run_test_case, test_case, cap)
                 time.sleep(5)

    def test_grid_serial(self,test_cases,user=None):
        self.user = user
        for caps in self.caps_list:
            for test_case in test_cases:
                self.run_test_case(test_case,caps)

    def run_test_case(self,test_case, caps=None):
        self.get_driver(caps,self.user)


    def run_single_browser(self,test_case=None):
        browser=self.config["browser"]
        if browser == "Chrome":
            #proxy_ip = 'localhost'  # Default ZAP Proxy IP
            #proxy_port = '8081'  # Default ZAP Proxy Port
            #zap_proxy = f"{proxy_ip}:{proxy_port}"

           # self.chrome_cap = webdriver.ChromeOptions()
           # self.chrome_cap.add_argument(f'--proxy-server={zap_proxy}')
           #self.chrome_cap.add_argument('--ignore-certificate-errors')
            self._driver = webdriver.Chrome()

        elif browser == "FireFox":
            self._driver = webdriver.Firefox()
        elif browser == "Edge":
            self._driver = webdriver.Edge()
        #if test_case!=None:
         #   test_case()

        #for cookie in self.cookies:
            #print(f"Current URL: {self._driver.current_url}")
            # Add the cookie for the current domain.

        self._driver.get("https://www.w3schools.com")
        self._driver.maximize_window()

    def teardown(self):
        self._driver.close()
        self._driver.quit()
