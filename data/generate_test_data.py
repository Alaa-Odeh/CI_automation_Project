import json
import random
import os

def load_basic_skills(filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_test_data(all_skills, goal_basic_skills):
    unique_skills = list(set(all_skills))
    test_data = []  # Initialize as a list to hold dictionaries
    levels = ['Beginner', 'Intermediate', 'Advanced', 'Professional']  # Example skill levels

    for skill in unique_skills:
        for goal_name, basic_skills in goal_basic_skills.items():
            if skill not in basic_skills:
                combined_skills = basic_skills + [skill]
                skill_levels = [random.choice(levels) for _ in combined_skills]
                hours_per_week = random.randint(1, 60)
                test_case = {
                    "goal_name": goal_name,
                    "skills": combined_skills,
                    "levels": skill_levels,  # Separate levels list
                    "hours_per_week": hours_per_week
                }
                test_data.append(test_case)  # Append the dictionary to the list

    return test_data

if __name__ == '__main__':
    goal_basic_skills = load_basic_skills('basic_skills.json')
    all_skills = [
        "Accessibility", "AngularJS", "ASP", "AWS Cloud", "AWS Serverless",
        "Bootstrap 3", "Bootstrap 4", "Bootstrap 5", "C", "C#", "C++",
        "CSS", "Cyber Security", "Data Science", "Django", "DSA", "Excel",
        "General problem solving and logical reasoning", "Git", "Go", "HTML", "Java",
        "JavaScript", "jQuery", "Kotlin", "MongoDB", "MySQL", "Node.js", "NumPy", "Pandas",
        "PHP", "PostgreSQL", "Python", "R", "React", "SASS", "SciPy", "SQL", "Statistics",
        "TypeScript", "Vue.js", "W3.CSS", "XML"
    ]
    test_data = generate_test_data(all_skills, goal_basic_skills)
    test_data_path = os.path.join(os.path.dirname(__file__), 'test_data.json')
    with open(test_data_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=4)
