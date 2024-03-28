pipeline {
    agent any
    environment {
        PYTHON_PATH = "C:\\Users\\Alaa Oda\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        PIP_PATH = "C:\\Users\\Alaa Oda\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\pip.exe"
        IMAGE_NAME = 'tests'
        TAG = 'latest'
    }
    stages {
        stage('Setup Environment') {
            steps {
                bat "call \"%PYTHON_PATH%\" -m venv venv"
                bat "call venv\\Scripts\\python.exe -m pip install --upgrade pip"
                bat "call venv\\Scripts\\pip.exe install -r requirements.txt"
                bat "call venv\\Scripts\\pip.exe install pytest pytest-html selenium"
            }
            post {
                success {
                    slackSend (color: 'good', message: "SUCCESS: Setup Environment stage completed successfully.")
                }
                failure {
                    slackSend (color: 'danger', message: "FAILURE: Setup Environment stage failed.")
                }
            }

        }
        stage('Setup Selenium Server HUB') {
            steps {
                echo 'Setting up Selenium server HUB...'
                bat "start /B java -jar selenium-server.jar --port 4445 --role hub"
                bat "ping 127.0.0.1 -n 11 > nul"
            }
            post {
                success {
                    slackSend (color: 'good', message: "SUCCESS: Setup Selenium Server HUB stage completed successfully.")
                }
                failure {
                    slackSend (color: 'danger', message: "FAILURE: Setup Selenium Server HUB stage failed.")
                }
            }
        }
        stage('Setup Selenium Server nodes') {
            steps {
                echo 'Setting up Selenium server nodes...'
                bat "start /B java -jar selenium-server.jar -role node --port 5555 --hub http://127.0.0.1:4445/grid/register"
                bat "ping 127.0.0.1 -n 11 > nul"
           }
            post {
                success {
                    slackSend (color: 'good', message: "SUCCESS: Setup Selenium Server nodes stage completed successfully.")
                }
                failure {
                    slackSend (color: 'danger', message: "FAILURE: Setup Selenium Server nodes stage failed.")
                }
            }
        }
        stage('Run Generated Tests with Pytest') {
            steps {
                echo 'Testing Generated tests'
                bat "call venv\\Scripts\\python.exe -m pytest -n auto tests/test_generate_tests/test_generate_api_test.py --html=Generated_Tests_report.html --self-contained-html"
            }
        }
        stage('Run API Tests with Pytest ') {
            steps {
                bat "call venv\\Scripts\\python.exe -m pytest test_runner.py"
            }
            post {
                success {
                    slackSend (color: 'good', message: "SUCCESS: Running Tests stage completed successfully.")
                }
                failure {
                    slackSend (color: 'danger', message: "FAILURE: Running Tests stage failed.")
                }
            }
        }
    }

    post {
        success {
            slackSend(channel: 'C06Q6FRSFKJ', color: "good", message: "Build succeeded")
        }
        failure {
            slackSend(channel: 'C06Q6FRSFKJ', color: "danger", message: "Build failed")
        }
        always {
            archiveArtifacts artifacts: "${env.TEST_REPORTS}/*.html", allowEmptyArchive: true
            echo 'Cleaning up...'
        }
    }
}