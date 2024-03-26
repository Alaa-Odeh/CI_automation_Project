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
                            bat "docker run --name web_test_container ${IMAGE_NAME}:${TAG} python -m tests/tests_runner.py"
                            bat "docker stop web_test_container"
                            bat "docker rm web_test_container"
                        },
                        'another Test': {
                            // Placeholder for an additional test suite
                            // Update the container name and test script as necessary
                            bat "docker run --name another_test_container ${IMAGE_NAME}:${TAG} python -m tests/another_tests_runner.py"
                            bat "docker stop another_test_container"
                            bat "docker rm another_test_container"
                        },
                    )
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            bat "docker stop web_test_container || true"
            bat "docker rm web_test_container || true"
            bat "docker stop another_test_container || true"
            bat "docker rm another_test_container || true"
            bat "docker rmi -f ${IMAGE_NAME}:${TAG}"
        }
    }
}
