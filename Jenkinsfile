pipeline {
    agent any

    environment {
        PYTHON = "python3"
        VENV = ".venv"
        ALLURE_RESULTS = "reports/allure"
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
                    jmeter -n -t jmeter-plan.jmx -l results.jtl
                """
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
