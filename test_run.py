import json
import subprocess
from pathlib import Path


def run_pytest(parallel=False):
    ui_tests_path = "tests/test_api"
    reports_dir = Path("tests/test_web/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Base command with the path to UI tests
    base_cmd = ["venv/Scripts/python.exe","-m","venv/Scripts/pytest.exe", ui_tests_path]
    html_report = str(reports_dir / "report.html")

    if parallel:
        # Run tests in parallel except those marked as 'serial'
        parallel_cmd = base_cmd + ["-n", "3", "-m", "not serial", f"--html={html_report}"]
    else:
        # Run all tests serially
        parallel_cmd = base_cmd + [f"--html={html_report}"]

    try:
        # Run the pytest command with subprocess
        subprocess.run(parallel_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with return code {e.returncode}. Continuing the build...")


if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)

    # Determine whether to run tests in parallel based on the config
    is_parallel = config["grid type"] == "parallel"
    run_pytest(parallel=is_parallel)
