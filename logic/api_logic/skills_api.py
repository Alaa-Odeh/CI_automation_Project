import json
from pathlib import Path

from infra.infra_api.api_wrapper import APIWrapper


class SkillsAPI:

    def __init__(self):
        self.api_object = APIWrapper()
        self.new_url = self.api_object.url + "competency-api/skills"
        cur_dir = Path(__file__).resolve().parents[0].parents[0].joinpath("Info_API.json")
        with open(cur_dir, 'r') as config_file:
            self.info_api = json.load(config_file)

    def get_skills(self):
        self.result = self.api_object.api_get_request(self.new_url).json()

    def get_skills_dict_by_name(self):
        self.get_skills()
        self.skills_dict = {item['name']: item['id'] for item in self.result if item.get('type') == 'skill'}
        return self.skills_dict
    def get_skills_dict_by_id(self):
        self.get_skills()
        self.skills_dict = {item['id']: item['name'] for item in self.result if item.get('type') == 'skill'}
        return self.skills_dict

    def create_body_for_skills(self,goal_name, skills_names, levels,hours_per_week):
        self.get_skills_dict_by_name()
        skill_ids = [self.skills_dict[skill] for skill in skills_names if skill in self.skills_dict]
        self.convert_course_levels_words_to_numbers(levels)
        skills_list = {skill_id: {"level": level} for skill_id, level in zip(skill_ids, self.levels)}
        self.body = {
            "name": goal_name,
            "skills": skills_list,
            "hoursPerWeek": hours_per_week  # Example, adjust as necessary
        }
        return self.body

    def convert_course_levels_numbers_to_words(self,levels):
        self.levels=[self.info_api["levels_dict"][level] for level in levels if level in self.info_api["levels_dict"]]

    def convert_course_levels_words_to_numbers(self,levels):
        self.levels=[self.info_api["levels_dict"][level] for level in levels if level in self.info_api["levels_dict"]]
    def generate_test_cases(self):
        basic_skills = ['C++', 'C#', 'JavaScript', 'DSA']
        self.get_skills_dict_by_name()
        basic_skills_id = [self.skills_dict[name] for name in basic_skills]
        all_skills = list(self.skills_dict.values())
        optional_skills = list(set(all_skills) - set(basic_skills_id))
        hardness_levels = [25, 50, 75, 90]
        total_skills = 6
        additional_skills_needed = total_skills - len(basic_skills_id)
        used_skills = set()  # Track which skills have been used
        self.all_test_cases=[[]]
        for skill in optional_skills:
            for other_skill in optional_skills:
                if skill != other_skill and other_skill not in used_skills:
                    for level1 in hardness_levels:
                        for level2 in hardness_levels:
                            test_skills = basic_skills_id + [skill, other_skill]
                            test_levels = [50] * len(basic_skills_id) + [level1, level2]
                            self.all_test_cases.append((test_skills, test_levels))
                            used_skills.add(skill)
                            used_skills.add(other_skill)
                            print(test_skills, test_levels)
                # Break out of the loop once all skills have been used at least once
                if len(used_skills) == len(optional_skills):
                    return


