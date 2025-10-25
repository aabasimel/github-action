pipeline {
    agent any
    
    stages {
        stage('Check System Dependencies') {
            steps {
                sh '''
                    echo "=== Checking System Dependencies ==="
                    echo "1. Checking Python..."
                    if command -v python3 >/dev/null 2>&1; then
                        echo "✅ Python3 found: $(python3 --version)"
                    else
                        echo "❌ ERROR: Python3 not found"
                        exit 1
                    fi
                '''
            }
        }
        
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/aabasimel/github-action.git'
            }
        }
        
        stage('Create Virtual Environment') {
            steps {
                sh '''
                    echo "=== Creating Python Virtual Environment ==="
                    python3 -m venv jenkins_venv
                    echo "Virtual environment created"
                    
                    # Activate venv and check Python
                    . jenkins_venv/bin/activate
                    python --version
                    pip --version
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "=== Installing Python Dependencies ==="
                    . jenkins_venv/bin/activate
                    
                    # Upgrade pip and install dependencies
                    pip install --upgrade pip
                    pip install pytest pytest-html
                    
                    # Install project dependencies
                    if [ -f requirements.txt ]; then
                        echo "Installing from requirements.txt"
                        pip install -r requirements.txt
                    else
                        echo "No requirements.txt found"
                    fi
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    echo "=== Running Tests ==="
                    . jenkins_venv/bin/activate
                    
                    # Create tests directory if needed
                    mkdir -p tests
                    
                    # Create sample test if no tests exist
                    if [ ! -f tests/test_example.py ]; then
                        echo "Creating sample test file..."
                        cat > tests/test_example.py << 'EOF'
def test_addition():
    """Test basic addition"""
    assert 1 + 1 == 2

def test_subtraction():
    """Test basic subtraction"""
    assert 5 - 3 == 2

def test_list_operations():
    """Test list operations"""
    assert len([1, 2, 3]) == 3

def test_string_operations():
    """Test string operations"""
    assert "hello".upper() == "HELLO"
    assert "WORLD".lower() == "world"
EOF
                    fi
                    
                    # Run tests with HTML report
                    echo "Running pytest..."
                    python -m pytest tests/ -v --html=test_report.html --self-contained-html
                    
                    echo "Test execution completed"
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
        
        stage('Cleanup') {
            steps {
                sh '''
                    echo "=== Cleaning Up ==="
                    # List generated files
                    echo "Generated files:"
                    ls -la *.html 2>/dev/null || echo "No HTML files"
                    echo "Virtual environment size:"
                    du -sh jenkins_venv 2>/dev/null || echo "No venv directory"
                '''
            }
        }
    }
    
    post {
        always {
            echo "=== Pipeline Execution Complete ==="
            echo "Check the 'Pytest Report' link for test results"
        }
        success {
            echo "✅ SUCCESS: Pipeline completed successfully!"
        }
        failure {
            echo "❌ FAILURE: Pipeline encountered errors"
        }
    }
}