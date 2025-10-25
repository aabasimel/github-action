pipeline {
    agent any
    
    tools {
        python 'python3'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                    pip install pytest pytest-html
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    python -m pytest tests/ -v --html=test_report.html --self-contained-html || true
                '''
            }
            post {
                always {
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'test_report.html',
                        reportName: 'Pytest Report'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed - check test reports for details'
        }
    }
}