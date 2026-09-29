pipeline {

    agent any

    environment {
        IMAGE_NAME = "jenkins-app:build-${BUILD_NUMBER}"
        CONTAINER_NAME = "jenkins-app"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/USERNAME/jenkins-docker-app.git'
            }
        }

        stage('Build Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Deploy & Verify') {
            steps {

                bat '''
                docker stop %CONTAINER_NAME% 2>NUL || exit 0
                docker rm %CONTAINER_NAME% 2>NUL || exit 0
                docker run -d --name %CONTAINER_NAME% -p 8081:80 %IMAGE_NAME%
                '''

                bat '''
                docker ps
                docker inspect --format="{{.State.Running}}" %CONTAINER_NAME%
                '''
            }
        }
    }
}