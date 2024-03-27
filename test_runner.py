import json
import subprocess


def run_pytest(parallel=False):
    ui_tests_path = "tests/test_api/test_update_goal_api.py"
    python_path = "venv/Scripts/python.exe"
    base_cmd = [python_path,"-m", "pytest", ui_tests_path, "--html=report.html"]

    if parallel:
        # Run tests in parallel except those marked as 'serial'
        base_cmd.extend(["-n", "4", "-m", "not serial"])
        subprocess.run(base_cmd)
    else:
        # Run all tests serially
        base_cmd.extend(["--html=report_serial.html"])

    subprocess.run(base_cmd)



if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)

    # Determine whether to run tests in parallel based on the config
    is_parallel = config["grid type"]
    run_pytest(parallel=is_parallel)
