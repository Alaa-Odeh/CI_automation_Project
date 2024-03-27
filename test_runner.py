import json
import subprocess


def run_pytest(parallel=False):
    ui_tests_path = "tests/test_api"

    base_cmd = ["pytest", ui_tests_path, "--html=report.html"]

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
    is_parallel = config["grid type"] == "parallel"
    run_pytest(parallel=is_parallel)
