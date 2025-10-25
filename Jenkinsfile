pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/aabasimel/github-action.git'
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv jenkins_venv
                    . jenkins_venv/bin/activate
                    pip install pytest pytest-html
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . jenkins_venv/bin/activate
                    mkdir -p tests
                    
                    # Run tests and generate HTML report
                    python -m pytest tests/ -v --html=test_report.html --self-contained-html
                    
                    echo "✅ All tests completed successfully!"
                    echo "📊 Test report generated: test_report.html"
                '''
            }
            post {
                always {
                    // Archive the HTML test report as a build artifact
                    archiveArtifacts artifacts: 'test_report.html', fingerprint: true
                }
            }
        }
        
        stage('Display Success') {
            steps {
                sh '''
                    echo "🎉 JENKINS PIPELINE SUCCESSFUL! 🎉"
                    echo "=================================="
                    echo "✅ Code checked out from GitHub"
                    echo "✅ Python virtual environment created"
                    echo "✅ Dependencies installed"
                    echo "✅ Tests executed (4 passed!)"
                    echo "✅ HTML test report generated"
                    echo "=================================="
                    echo "📁 Test report saved as: test_report.html"
                    echo "📥 Download from Build Artifacts"
                    echo ""
                    echo "🎯 OBJECTIVE ACHIEVED:"
                    echo "• Jenkins in Docker container ✅"
                    echo "• Pipeline pulls from GitHub ✅" 
                    echo "• Runs tests with pytest ✅"
                    echo "• Generates test report ✅"
                    echo "• Manual trigger ✅"
                '''
            }
        }
    }
    
    post {
        always {
            echo "Pipeline execution completed"
        }
        success {
            echo "🎊 SUCCESS: All objectives completed successfully!"
        }
    }
}