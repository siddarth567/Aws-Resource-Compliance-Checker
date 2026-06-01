pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/siddarth567/aws-compliance-checker.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aws-compliance-checker .'
            }
        }

        stage('Run Compliance Scan') {
            steps {
                sh '''
                docker run --rm \
                -v $HOME/.aws:/root/.aws \
                aws-compliance-checker
                '''
            }
        }
    }
}
