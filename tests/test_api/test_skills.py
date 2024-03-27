import os
import unittest
from pathlib import Path
from dotenv import load_dotenv
from infra.infra_api.api_wrapper import APIWrapper
from logic.api_logic.skills_api import SkillsAPI
from pytest_markers import test_decorator


class TestSkills(unittest.TestCase):
    def setUp(self):
        self.my_api = APIWrapper()
        self.url = self.my_api.url
        self.skills = SkillsAPI()

    @test_decorator
    def test_get_response_skills(self):
        self.skills.get_skills()
        self.skills.get_skills_dict_by_name()
        print(self.skills.skills_dict)

    @test_decorator
    def test_generate_test_cases(self):
        self.skills.get_skills()
        self.skills.generate_test_cases()
        print(self.skills.all_test_cases[0])



