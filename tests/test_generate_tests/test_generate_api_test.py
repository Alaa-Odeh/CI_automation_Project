import pytest
from logic.api_logic.goals_api import GoalsAPI


# Your setup code can be refactored into a pytest fixture
@pytest.fixture(scope="function")
def goals_api():
    api = GoalsAPI()
    yield api
    api.delete_goal()  #tearDown
    ##
# Use pytest.mark.parametrize to create variations
@pytest.mark.parametrize(
    "goal_name, skills, levels, hours_per_week", [
        ("Game developer", ["HTML", "C#", "C++"], ["Professional", "Advanced", "Intermediate"], 10),
        ("Frontend developer", [ "Python","HTML"], ["Beginner", "Intermediate"], 10)
                # Add more variations here as tuples
    ])
def test_generate_api_test(goals_api, goal_name, skills, levels, hours_per_week):
    goals_api.post_new_goal(goal_name, skills, levels, hours_per_week)
    skill_names, skill_levels, updated_hours_per_week = goals_api.get_goal_info()

    assert sorted(skill_names) == sorted(skills), "Skills do not match"
    assert sorted(skill_levels) == sorted(levels), "Levels do not match"
    assert updated_hours_per_week == hours_per_week, "Weekly hours not updated"
