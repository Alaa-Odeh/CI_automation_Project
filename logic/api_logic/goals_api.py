
from infra.infra_api.api_wrapper import APIWrapper
from logic.api_logic.skills_api import  SkillsAPI


class GoalsAPI:
    def __init__(self):
        self.api_object = APIWrapper()
        self.skills=SkillsAPI()
        self.new_url = self.api_object.url+"goals-api/goals"

    def get_goals(self):
        response = self.api_object.api_get_request(self.new_url)
        if response and hasattr(response, 'json'):
            self.result = response.json()
        else:
            self.result = None


    def post_a_goal(self,body):
        self.result = self.api_object.api_post_request(self.new_url,body)

    def update_a_goal(self,new_url,body):
        self.result = self.api_object.api_put_request(new_url,body)


    def post_new_goal(self,goal_name,skills_name,levels,hours_per_week):
        self.skills.create_body_for_skills(goal_name,skills_name,levels,hours_per_week)
        self.post_a_goal(self.skills.body)

    def get_goal_id(self,):
        self.get_goals()
        if self.result != None:
            if  len(self.result.keys())!= 0:
                return list(self.result.keys())[0]
        else:
            return "No Goals Exist"

    def delete_goal(self,):
        self.get_goals()
        goal_id=self.get_goal_id()
        if goal_id is not None:
            self.new_url=self.new_url+f'/{goal_id}'
            self.api_object.api_delete_request(self.new_url)
        else:
            return "No Goals Exist"

    def get_goal_info(self,expected_skills):
        goal_id=self.get_goal_id()
        self.new_url = self.new_url + f'/{goal_id}'
        self.result = self.api_object.api_get_request(self.new_url).json()
        self.result_skills=self.result['skills']
        skills_dict = self.skills.get_skills_dict_by_id()
        levels_dict = self.skills.info_api["levels_dict"]
        skills_info = {}

        for skill_id, details in self.result_skills.items():
            skill_name = skills_dict.get(skill_id)
            if skill_name in expected_skills:
                level_number = details['level']
                # Find the corresponding level name from the levels dictionary
                level_name = next((name for name, number in levels_dict.items() if number == level_number), None)
                skills_info[skill_name] = level_name

        # Now reorder the skills based on the expected_skills list and convert levels
        ordered_skill_names = []
        ordered_skill_levels = []

        for skill in expected_skills:
            if skill in skills_info:
                ordered_skill_names.append(skill)
                ordered_skill_levels.append(skills_info[skill])
        return ordered_skill_names, ordered_skill_levels,self.result['hoursPerWeek']

    def update_an_existing_goal(self,goal_name,skills_name,levels,hours_per_week):
        self.skills.create_body_for_skills(goal_name,skills_name,levels,hours_per_week)
        goal_id = self.get_goal_id()
        new_url = self.new_url + f'/{goal_id}'
        self.update_a_goal(new_url,self.skills.body)