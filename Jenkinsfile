jenkinsfile
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


        stage('Run Tests in Parallel') {
            steps {
                script {
                    parallel(
                        'web Test': {
                            // Correct the docker run command to point to the correct script file
                            bat "docker run --name web_test_container ${IMAGE_NAME}:${TAG} python -m tests/tests_runner.py"
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