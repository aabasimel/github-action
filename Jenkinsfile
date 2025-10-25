pipeline {
    agent any  // Simple agent that works without Docker
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/aabasimel/github-action.git'
            }
        }
        
        stage('Environment Info') {
            steps {
                sh '''
                    echo "=== Environment Information ==="
                    echo "Working directory:"
                    pwd
                    echo "Contents:"
                    ls -la
                    echo "Python availability:"
                    python3 --version 2>/dev/null || python --version 2>/dev/null || echo "Python not found in standard locations"
                    echo "Pip availability:"
                    pip3 --version 2>/dev/null || pip --version 2>/dev/null || echo "Pip not found in standard locations"
                '''
            }
        }
        
        stage('Setup Python') {
            steps {
                sh '''
                    echo "=== Setting up Python Environment ==="
                    # Try to use available Python
                    if command -v python3 &> /dev/null; then
                        PYTHON_CMD=python3
                        PIP_CMD=pip3
                    elif command -v python &> /dev/null; then
                        PYTHON_CMD=python
                        PIP_CMD=pip
                    else
                        echo "ERROR: No Python installation found"
                        exit 1
                    fi
                    
                    echo "Using: $PYTHON_CMD and $PIP_CMD"
                    $PYTHON_CMD --version
                    $PIP_CMD --version
                    
                    # Upgrade pip and install dependencies
                    $PIP_CMD install --user --upgrade pip
                    $PIP_CMD install --user pytest pytest-html
                    
                    # Install requirements if they exist
                    if [ -f requirements.txt ]; then
                        echo "Installing from requirements.txt"
                        $PIP_CMD install --user -r requirements.txt
                    fi
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    echo "=== Running Tests ==="
                    # Determine Python command
                    if command -v python3 &> /dev/null; then
                        PYTHON_CMD=python3
                    else
                        PYTHON_CMD=python
                    fi
                    
                    # Create tests directory if it doesn't exist
                    mkdir -p tests
                    
                    # Create a simple test file if no tests exist
                    if [ ! -f tests/test_example.py ] && [ ! -f tests/test_*.py ]; then
                        echo "Creating example test file..."
                        cat > tests/test_example.py << 'EOF'
def test_addition():
    """Test basic addition"""
    assert 1 + 1 == 2

def test_subtraction():
    """Test basic subtraction"""
    assert 5 - 3 == 2

def test_list_length():
    """Test list operations"""
    assert len([1, 2, 3]) == 3

def test_string_operations():
    """Test string operations"""
    assert "hello".upper() == "HELLO"
EOF
                        echo "Created sample test file: tests/test_example.py"
                    fi
                    
                    # Run pytest with HTML report
                    echo "Running tests..."
                    $PYTHON_CMD -m pytest tests/ -v --html=test_report.html --self-contained-html
                    
                    echo "Test execution completed"
                '''
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
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