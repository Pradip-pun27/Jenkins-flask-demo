pipeline {
    agent any

    environment {
        APP_NAME = "flask-live-app"
        APP_PORT = "5000"
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Pulling latest code commit from GitHub...'
                checkout scm
            }
        }

        stage('2. Run CI Tests') {
            steps {
                echo 'Creating temporary virtualenv and running unit tests...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest test_app.py
                '''
            }
        }

        stage('3. Build Docker Image') {
            steps {
                echo 'Building Docker Image from Dockerfile...'
                sh "docker build -t ${APP_NAME}:latest ."
            }
        }

        stage('4. Deploy Container on EC2') {
            steps {
                echo 'Replacing running container with new build...'
                sh '''
                    # Stop and remove existing container if running
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true

                    # Start updated container on port 5000
                    docker run -d --restart unless-stopped -p ${APP_PORT}:5000 --name ${APP_NAME} ${APP_NAME}:latest
                '''
            }
        }

        stage('5. Smoke Test') {
            steps {
                echo 'Running endpoint verification...'
                sleep 5
                sh "curl -f http://localhost:${APP_PORT}/health"
            }
        }
    }

    post {
        always {
            sh 'rm -rf venv'
        }
        success {
            echo "CI/CD Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed. Deployment halted."
        }
    }
}
