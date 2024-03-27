pipeline {
    agent any
    environment {
        PYTHON_PATH = "C:\\Users\\Alaa Oda\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        PIP_PATH = '"C:\\Users\\Alaa Oda\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\pip.exe"'
        TEST_REPORTS = 'test-reports'
        IMAGE_NAME = 'tests'
        TAG = 'latest'
    }
    stages {
        stage('Setup Environment') {
            steps {
                bat 'call "%PYTHON_PATH%" -m venv venv'
                bat 'call venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat 'call venv\\Scripts\\pip.exe install -r requirements.txt'
                bat 'call venv\\Scripts\\pip.exe install pytest pytest-html selenium'
            }
        }
        stage('Setup Selenium Server HUB') {
            steps {
                echo 'Setting up Selenium server HUB...'
                bat "start /B java -jar selenium-server.jar hub"
                // Delay for 10 seconds
                bat 'ping 127.0.0.1 -n 11 > nul' // Windows command to sleep for 10 seconds
            }
        }
        stage('Setup Selenium Server nodes') {
            steps {
                echo 'Setting up Selenium server nodes...'
                bat "start /B java -jar selenium-server.jar node --port 5555 --selenium-manager true"
                // Delay for 10 seconds
                bat 'ping 127.0.0.1 -n 11 > nul' // Windows command to sleep for 10 seconds
            }
        }
        stage('Check Directory and File') {
    steps {
        script {
                // For Windows Batch Command
                bat """
                echo Checking directory...
                dir
                echo Checking if tests_runner.py exists...
                if exist tests/tests_runner.py (
                    echo tests_runner.py exists
                ) else (
                    echo tests_runner.py does not exist
                )
                """
            }
        }
    }


         stage('Run Tests with Pytest') {
            steps {
                script {
                    // Here you determine the number of parallel workers, can be set to a fixed value or dynamically based on CPU cores
                    def cpuCount = Runtime.runtime.availableProcessors()
                    bat "call venv\\Scripts\\pytest.exe -n ${cpuCount} tests\\test_generate_tests\\ --html=${TEST_REPORTS}\\report.html --self-contained-html"
                }
            }
         }
    }
    post {
        success {
                slackSend(channel: 'C06Q6FRSFKJ',color: "good", message: "Build succeeded")
            }
        failure {
            slackSend(channel: 'C06Q6FRSFKJ',color: "danger", message: "Build failed")
        }
        always {
            archiveArtifacts artifacts: "${TEST_REPORTS}/*.html", allowEmptyArchive: true
            echo 'Cleaning up...'

        }
    }
}