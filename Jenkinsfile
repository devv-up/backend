pipeline {
    agent { dockerfile true }
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
    stages {
        stage ('Lint') {
            parallel {
                stage('flake8') {
                    steps {
                        sh 'flake8'
                    }
                }
                stage('isort') {
                    steps {
                        sh 'isort -c'
                    }
                }
                stage('mypy') {
                    steps {
                        sh 'mypy .'
                    }
                }
            }
        }
        stage ('Test') {
            steps {
                sh 'pytest'
            }
        }
    }
}
