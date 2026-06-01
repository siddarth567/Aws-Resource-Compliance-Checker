pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'sudo docker build -t aws-compliance-checker .'
            }
        }

        stage('Run Compliance Scan') {
            steps {
                sh '''
                sudo docker run --rm \
                --network host \
                aws-compliance-checker
                '''
            }
        }

        stage('Archive Report') {
            steps {
                archiveArtifacts artifacts: 'reports/compliance_report.txt', fingerprint: true
            }
        }
    }
}
