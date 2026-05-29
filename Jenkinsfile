pipeline {
    agent any

    environment {
        PYTHON = "python3"
        VENV = ".venv"
        ALLURE_RESULTS = "reports/allure"
        LOCUST_FILE = "tests/performance/locustfile.py"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh """
                    ${PYTHON} -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Start Test Services (Docker)') {
            steps {
                sh "docker-compose up -d"
                sh "sleep 10"
            }
        }

        stage('Static Analysis') {
            steps {
                sh """
                    . ${VENV}/bin/activate
                    flake8 src tests
                """
            }
        }

        stage('Unit Tests') {
            steps {
                sh """
                    . ${VENV}/bin/activate
                    pytest tests/unit --alluredir=${ALLURE_RESULTS}/unit
                """
            }
        }

        stage('Integration Tests') {
            steps {
                sh """
                    . ${VENV}/bin/activate
                    pytest tests/integration --alluredir=${ALLURE_RESULTS}/integration
                """
            }
        }

        stage('API Tests') {
            steps {
                sh """
                    . ${VENV}/bin/activate
                    pytest tests/api --alluredir=${ALLURE_RESULTS}/api
                """
            }
        }

        stage('Security Tests') {
            steps {
                sh """
                    . ${VENV}/bin/activate
                    pytest tests/security --alluredir=${ALLURE_RESULTS}/security
                """
            }
        }

        stage('Performance Tests (Optional)') {
            when {
                expression { return params.RUN_PERFORMANCE_TESTS == true }
            }
            steps {
                sh """
                    . ${VENV}/bin/activate
                    locust -f ${LOCUST_FILE} \
                        --headless \
                        --users 50 \
                        --spawn-rate 10 \
                        --run-time 5m \
                        --html locust_report.html
                """
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'locust_report.html', fingerprint: true
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: "reports/allure"]]
            sh "docker-compose down"
        }
    }
}
