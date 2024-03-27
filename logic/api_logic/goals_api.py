
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

    def delete_goal(self):
        self.get_goals()
        goal_id=self.get_goal_id()
        if goal_id is not None:
            delete_url=self.new_url+f'/{goal_id}'
            try:
                response = self.api_object.api_delete_request(delete_url)
                if response.status_code == 200:
                    return True
                else:
                    # Log error or raise an exception
                    return False
            except Exception as e:
                # Log the exception or handle it as per your needs
                return False
            return False  # Returns false if there was no goal to delete

    def get_goal_id_by_name(self, goal_name):
        self.get_goals()
        if self.result is not None:
            for id, details in self.result.items():
                if 'name' in details and details['name'] == goal_name:
                    return id
        return None
    def get_goal_info(self,goal_name):
        goal_id = self.get_goal_id_by_name(goal_name)
        self.new_url = self.new_url + f'/{goal_id}'
        self.result = self.api_object.api_get_request(self.new_url).json()
        self.result_skills = self.result['skills']
        skills_dict = self.skills.get_skills_dict_by_id()
        levels_dict = self.skills.info_api["levels_dict"]

        # Lists to store the retrieved skills and levels
        retrieved_skill_names = []
        retrieved_skill_levels = []

        # Iterate over the skills in the goal
        for skill_id, details in self.result_skills.items():
            skill_name = skills_dict.get(skill_id)
            level_number = details['level']
            # Find the corresponding level name from the levels dictionary
            level_name = next((name for name, number in levels_dict.items() if number == level_number), None)
            retrieved_skill_names.append(skill_name)
            retrieved_skill_levels.append(level_name)

        return retrieved_skill_names, retrieved_skill_levels, self.result['hoursPerWeek']

    def update_an_existing_goal(self,goal_name,skills_name,levels,hours_per_week):
        self.skills.create_body_for_skills(goal_name,skills_name,levels,hours_per_week)
        goal_id = self.get_goal_id()
        new_url = self.new_url + f'/{goal_id}'
        self.update_a_goal(new_url,self.skills.body)