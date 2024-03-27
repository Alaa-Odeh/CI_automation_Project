pipeline {
    agent any
    environment {
        PYTHON_PATH = "C:\\Users\\Alaa Oda\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        PIP_PATH = "C:\\Users\\Alaa Oda\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\pip.exe"
        TEST_REPORTS = 'test-reports'
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
        }
        stage('Setup Selenium Server HUB') {
            steps {
                echo 'Setting up Selenium server HUB...'
                bat "start /B java -jar selenium-server.jar --port 4445 --role hub"
                bat "ping 127.0.0.1 -n 11 > nul"
            }
        }
        stage('Setup Selenium Server nodes') {
            steps {
                echo 'Setting up Selenium server nodes...'
                bat "start /B java -jar selenium-server.jar -role node --port 5555 --hub http://127.0.0.1:4445/grid/register"
                bat "ping 127.0.0.1 -n 11 > nul"
            }
        }
        stage('Run Tests with Pytest') {
            steps {
                //bat "call venv\\Scripts\\python.exe -m pytest tests\\test_generate_tests --html=${env.TEST_REPORTS}\\report.html --self-contained-html"
                bat "call venv\\Scripts\\python.exe -m pytest tests/test_generate_tests/test_generate_api_test.py"
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