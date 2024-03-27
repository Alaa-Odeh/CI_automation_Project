import concurrent


def create_test_case(goal_name, skills, levels, hours_per_week):
    return type(
        f'TestAPI_{goal_name}',
        (TestAPITemplate,),
        {
            'goal_name': goal_name,
            'skills': skills,
            'levels': levels,
            'hours_per_week': hours_per_week
        }
    )

def run_test_case(test_class):
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_class))
    runner = unittest.TextTestRunner()
    runner.run(suite)

# Test variations
test_cases = [
    ('Game developer', ['HTML', 'C#', 'C++'], ['Professional', 'Advanced', 'Intermediate'], 10),
    ('Frontend developer', ['Python', 'HTML'], ['Beginner', 'Intermediate'], 10),
]

# Running tests in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(run_test_case, [create_test_case(*params) for params in test_cases])