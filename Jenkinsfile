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
                echo 'Setting up virtualenv and running unit tests...'
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest test_app.py
                """
            }
        }

        stage('3. Build Docker Image') {
            steps {
                echo "Building Docker Image: ${APP_NAME}:latest..."
                sh "docker build -t ${APP_NAME}:latest ."
            }
        }

        stage('4. Deploy Container on EC2') {
            steps {
                echo 'Deploying updated container...'
                sh """
                    # Stop and remove existing container if running
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true

                    # Start updated container on port 5000
                    docker run -d --restart unless-stopped -p ${APP_PORT}:5000 --name ${APP_NAME} ${APP_NAME}:latest
                """
            }
        }

        stage('5. Smoke Test') {
            steps {
                echo 'Verifying container health endpoint...'
                // Retries curl 5 times with a 2-second interval before declaring failure
                sh """
                    for i in {1..5}; do
                        if curl -s -f http://localhost:${APP_PORT}/health; then
                            echo " Service is healthy!"
                            exit 0
                        fi
                        echo "Waiting for container to initialize... (attempt \$i/5)"
                        sleep 2
                    done
                    echo "Service failed health check!"
                    exit 1
                """
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