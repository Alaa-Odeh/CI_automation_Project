pipeline {
    agent any

    environment {
        // Define the Docker image name
        IMAGE_NAME = 'tests'
        TAG = 'latest'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    def customImage = docker.build("${IMAGE_NAME}:${TAG}")
                }
            }
        }

        stage('Run API Tests in Parallel') {
            steps {
                script {
                    parallel(
                        'API Test': {
                            // Correct the docker run command to point to the correct script file
                            bat "docker run --name api_test_container ${IMAGE_NAME}:${TAG} python -m unittest discover -s tests/test_api -p test_log_in_page.Login_Page_Test.test_run.py"
                            // Ensure the container is stopped before removing it
                            bat "docker stop api_test_container"
                            bat "docker rm api_test_container"
                        },
                        // Add other parallel tests here as necessary
                    )
                }
            }
        }
        stage('Run Tests in Parallel') {
            steps {
                script {
                    parallel(
                        'web Test': {
                            // Correct the docker run command to point to the correct script file
                            bat "docker run --name web_test_container ${IMAGE_NAME}:${TAG} python -m unittest discover -s tests/test_web -p test_log_in_page.test_run.py"
                            // Ensure the container is stopped before removing it
                            bat "docker stop web_test_container"
                            bat "docker rm web_test_container"
                        },
                        // Add other parallel tests here as necessary
                    )
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Stop and remove any stray containers that might be using the image
            // Use the correct container names as per the tests run
            bat "docker stop api_test_container || true"
            bat "docker rm api_test_container || true"
            bat "docker stop web_test_container || true"
            bat "docker rm web_test_container || true"
            // Force remove the Docker image, if necessary, to clean up
            bat "docker rmi -f ${IMAGE_NAME}:${TAG}"
        }
    }
}