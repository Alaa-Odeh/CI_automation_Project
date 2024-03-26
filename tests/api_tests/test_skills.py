import os
import unittest
from pathlib import Path
from dotenv import load_dotenv
from infra.infra_api.api_wrapper import APIWrapper
from logic.api_logic.skills_api import Skills


class TestSkills(unittest.TestCase):
    def setUp(self):
        self.my_api = APIWrapper()
        self.url = self.my_api.url
        env_path = Path(__file__).resolve().parent.parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        self.token ="eyJraWQiOiJQS0tER0N2cFwvdlpVa1NEZDByem9NRTFEbWNDdElFM3o1V2ZmT0RMWWxJTT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJlZjcwOGQxZS0zOTc0LTQzNTctOTkxNy03MGMwOGMyZmNkNWIiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfdUc5U0dYN1dkX0dvb2dsZSJdLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV91RzlTR1g3V2QiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiJkMWdycW1sMGVtaDd2b3RrYjBndHJybjAiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIG9wZW5pZCIsImF1dGhfdGltZSI6MTcxMTAxMTk4OSwiZXhwIjoxNzExMDU1MTg5LCJpYXQiOjE3MTEwMTE5OTAsImp0aSI6IjY0Y2JkMzRkLWE5ZjUtNDc4Ny04MTdiLWZkZmZlNzE4OWUwMiIsInVzZXJuYW1lIjoiR29vZ2xlXzExNTU0MjYzNDE3OTA1OTgwMTk4OSJ9.GU0JhxKFi8QNNynymtOVKTwe9IE17L47542CmO6i_bjOYRIm37TEJ08sn_CppR6KWtDhNDeuH81O6TMEZL89lL7BAVB2EfXoX4-M4tqB6Plj6ddKWIPtG0YAl6tuv9Nrdu_Q290lrsBOpYOpeFJKgouForZfkMi2x39lCIgdPxTBgLd9qR42tlyZk-1W6avbxdtc9Yekfl7EX6YW5t8UK43YKlRKcxR7vJcAnWaQdRnbISZrxxyNXp5mBZ8NZqbFRkhquxgmA5b6d3DTJxCeqlLQMn8OsrM9ukfPNr-_Eq1cysadNeXxB2-RMTaBqcDzH9_w723GKAF_hyAJgfVhKw"
        self.skills = Skills(self.my_api, self.url, self.token)
    def test_get_response_skills(self):
        self.skills.get_skills()
        self.skills.get_skills_dict_by_name()
        print(self.skills.skills_dict)

    def test_generate_test_cases(self):
        self.skills.get_skills()
        self.skills.generate_test_cases()
        print(self.skills.all_test_cases[0])



