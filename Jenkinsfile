def findComment() {
  for (comment in pullRequest.comments) {
    if (comment.body.startsWith("[Jenkins]")) {
      return comment
    }
  }
  comment = pullRequest.comment("[Jenkins]")
  return comment
}

pipeline {
    agent {
        docker {
            image 'python:3.8'
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
        stage ('Wakeup') {
            steps {
                sh 'curl https://test.dev-up.kr/api/${GIT_BRANCH}'
                script {
                    if (env.GIT_BRANCH) {
                        pullRequest.editComment(comment.id, "[Jenkins]\n" + "https://test.dev-up.kr/api/" + env.GIT_BRANCH + "\n")
                    }
                }
            }
        }
    }
}
