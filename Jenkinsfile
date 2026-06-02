pipeline {
    agent any

    stages {
        stage('Checkout Source Code') {
            steps {
                git branch: 'main', url: 'https://github.com/siddarth567/Aws-Resource-Compliance-Checker.git'
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
                mkdir -p reports

                # Clean up any leftover container from previous runs
                docker rm -f compliance-runner || true

                # Create the container
                docker create --name compliance-runner --network host aws-compliance-checker

                # Run the container and show output
                docker start -a compliance-runner

                # Copy the generated report file from the container to Jenkins workspace
                docker cp compliance-runner:/app/reports/compliance_report.txt ./reports/compliance_report.txt

                # Clean up the container
                docker rm compliance-runner
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
