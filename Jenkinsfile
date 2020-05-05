pipeline {
    agent {
        docker {
            image 'python:alpine3.11'
        }
    }
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
    stages {
        stage ('Build') {
            steps {
                sh 'python -m venv .env'
                sh '.env/bin/pip install -r requirements.txt'
            }
        }
        stage ('Lint') {
            parallel {
                stage('flake8') {
                    steps {
                        sh '.env/bin/flake8'
                    }
                }
                stage('isort') {
                    steps {
                        sh '.env/bin/isort -c'
                    }
                }
                stage('mypy') {
                    steps {
                        sh '.env/bin/mypy .'
                    }
                }
            }
        }
        stage ('Test') {
            steps {
                sh '.env/bin/pytest --ds=dev_up.jenkins'
            }
        }
    }
}
