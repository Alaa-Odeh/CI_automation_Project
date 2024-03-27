import json
import os
import subprocess
import unittest
from pathlib import Path

def run_pytest(parallel=False):
    cur_dir = Path(__file__).resolve().parents[1].parents[0].joinpath("config.json")
    with open(cur_dir, 'r') as config_file:
        config = json.load(config_file)
    # Directory where all tests are located
    ui_tests_path = "tests/test_api/test_delete_goal_api.py"
    reports_dir = "tests/test_web/reports"
    print(ui_tests_path)
    os.makedirs(reports_dir, exist_ok=True)
    python_path = os.path.join("venv", "Scripts", "python.exe")
    # Basic command with the path to UI tests
    base_cmd = [python_path,"-m", "pytest",ui_tests_path]
    html_report = os.path.join(reports_dir, "report.html")
    # If parallel execution is enabled, modify the command to run with xdist
    if parallel:
        parallel_cmd = base_cmd + ["-n", "3", "-m", "not serial", f"--html={html_report}"]
        try:
            subprocess.run(parallel_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Tests failed with return code {e.returncode}. Continuing the build...")
    try:
        serial_html_report = os.path.join(reports_dir, "report_serial.html")
        serial_cmd = base_cmd + ["-m", "serial", f"--html={serial_html_report}"]
        subprocess.run(serial_cmd, check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 5:  # No tests were collected
            print("No serial tests were found.")
        else:
            print(e.returncode)
    else:
        non_parallel_cmd = base_cmd + [f"--html={html_report}"]
        try:
            subprocess.run(non_parallel_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(e.returncode)




def test_run():
    cur_dir = Path(__file__).resolve().parents[1].parents[0].joinpath("config.json")
    with open(cur_dir, 'r') as config_file:
        config = json.load(config_file)

    is_parallel=config["grid type"]

    run_pytest(parallel=is_parallel)
