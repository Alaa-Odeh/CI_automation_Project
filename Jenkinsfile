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
                bat "start /B java -jar selenium-server.jar hub"
                bat "ping 127.0.0.1 -n 11 > nul"
            }
        }
        stage('Setup Selenium Server nodes') {
            steps {
                echo 'Setting up Selenium server nodes...'
                bat "start /B java -jar selenium-server.jar node --port 5555 --selenium-manager true"
                bat "ping 127.0.0.1 -n 11 > nul"
            }
        }
        stage('Run Tests with Pytest') {
            steps {
                // Assuming '8' is the number of workers you want to use
                bat "call venv\\Scripts\\python.exe -m pytest tests\\test_generate_tests --html=${TEST_REPORTS}\\report.html --self-contained-html"
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
            archiveArtifacts artifacts: "${TEST_REPORTS}/*.html", allowEmptyArchive: true
            echo 'Cleaning up...'
        }
    }
}
