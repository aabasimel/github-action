pipeline {
    agent {
        docker { 
            image 'python:3.12-slim' 
            args '-u root:root' // optional: run as root for installing packages if needed
        }
    }
    environment {
        PYTHON_CMD = 'python'
        PIP_CMD = 'pip'
    }
    stages {
        stage('Check Python') {
            steps {
                sh '''
                    echo "Using: $PYTHON_CMD and $PIP_CMD"
                    $PYTHON_CMD --version
                    $PIP_CMD --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    $PIP_CMD install --upgrade pip
                    if [ -f requirements.txt ]; then
                        $PIP_CMD install -r requirements.txt
                    fi
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    if [ -f pytest.ini ] || [ -d tests ]; then
                        $PYTHON_CMD -m pytest --junitxml=results.xml
                    else
                        echo "No tests found, skipping..."
                    fi
                '''
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }

        stage('Final Report') {
            steps {
                echo "✅ Pipeline execution complete. Check the 'Pytest Report' for test results."
            }
        }
    }

    post {
        failure {
            echo "❌ FAILURE: Pipeline encountered errors"
        }
    }
}
