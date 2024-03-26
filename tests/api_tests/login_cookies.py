import base64
import hashlib
import os
import time
import unittest
from urllib.parse import urlparse,parse_qs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from infra.infra_web.browser_wrapper import BrowserWrapper
from logic.web_logic.home_page_pathfinder import PathfinderPage
from logic.web_logic.login_page import LoginPage
from logic.web_logic.welcome_page import WelcomePage
from selenium import webdriver
import requests
from zapv2 import ZAPv2
from selenium.webdriver.chrome.options import Options as ChromeOptions
class Login_Page_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate the code_verifier and code_challenge before the test starts
        cls.code_verifier = cls.generate_code_verifier()
        cls.code_challenge = cls.generate_code_challenge(cls.code_verifier)
        print(f"Code Verifier: {cls.code_verifier}")
        print(f"Code Challenge: {cls.code_challenge}")

    @staticmethod
    def generate_code_verifier():
        # Generate 32 bytes of random data
        token = os.urandom(32)
        # Base64 encode the data in a URL-safe manner, without padding
        code_verifier = base64.urlsafe_b64encode(token).rstrip(b'=').decode('utf-8')
        return code_verifier

    @staticmethod
    def generate_code_challenge(code_verifier):
        # Create a code_challenge based on the code_verifier
        return base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode(
            'utf-8')

    def test_log_in(self):

        driver=webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://profile.w3schools.com/")
        self.login_page = LoginPage(driver)
        self.login_page.login_flow("friendola15@gmail.com", "AutomationTester2024")
        WebDriverWait(driver, 25).until(EC.url_contains("profile.w3schools.com"))
        time.sleep(5)
        # Step 2: Capture the Authorization Code
        # This part is done after Selenium has navigated to the redirect_uri
        redirected_url = driver.current_url  # URL after user has authorized and been redirected
        parsed_url = urlparse(redirected_url)
        authorization_code = parse_qs(parsed_url.query).get('code')[0]

        # Step 3: Exchange the Authorization Code for an Access Token
        token_endpoint = 'https://auth.w3spaces.com/oauth2/token'  # Replace with actual token endpoint
        client_id = "d1grqml0emh7votkb0gtrrn0"
        redirect_uri = "https://profile.w3schools.com"

        data_payload = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'code_verifier': self.code_verifier
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'  # Set the correct Content-Type
        }
        print(data_payload)
        # Make the POST request to the token endpoint
        try:
            response = requests.post(token_endpoint, data=data_payload,headers=headers)
            response.raise_for_status()
            response_json = response.json()
            access_token = response_json.get('access_token')
            if access_token:
                print("Access Token:", access_token)
            else:
                raise Exception('Access token not found in the response')

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response Body: {response.text}")
            driver.quit()  # Close the browser window
            raise

        driver.quit()  # Close the browser window