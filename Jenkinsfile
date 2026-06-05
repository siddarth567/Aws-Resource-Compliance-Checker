pipeline {
    agent any

    triggers {
        cron('0 20 * * *')
    }

    parameters {
        string(
            name: 'EMAIL_RECIPIENT',
            defaultValue: 'ksiddharth263@gmail.com',
            description: 'Email address to send compliance report'
        )
    }

    stages {

        stage('Checkout Source Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/siddarth567/Aws-Resource-Compliance-Checker.git'
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

                docker rm -f compliance-runner || true

                docker create \
                    --name compliance-runner \
                    --network host \
                    aws-compliance-checker

                docker start -a compliance-runner

                docker cp \
                    compliance-runner:/app/reports/compliance_report.txt \
                    ./reports/compliance_report.txt

                docker rm compliance-runner
                '''
            }
        }

        stage('Archive Report') {
            steps {
                archiveArtifacts(
                    artifacts: 'reports/compliance_report.txt',
                    fingerprint: true
                )
            }
        }

        stage('Send Slack Notification') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'SLACK_WEBHOOK',
                        variable: 'SLACK_WEBHOOK_URL'
                    )
                ]) {

                    sh """
                    curl -X POST \
                    -H 'Content-type: application/json' \
                    --data '{
                        "text":"🚨 AWS Compliance Scan Completed\\n\\nJob: ${JOB_NAME}\\nBuild: #${BUILD_NUMBER}\\nStatus: SUCCESS\\n\\nReport: ${BUILD_URL}artifact/reports/compliance_report.txt"
                    }' \
                    \$SLACK_WEBHOOK_URL
                    """
                }
            }
        }
    }

    post {
        always {
            script {

                if (fileExists('reports/compliance_report.txt')) {

                    def reportContent = readFile(
                        'reports/compliance_report.txt'
                    )

                    mail(
                        to: params.EMAIL_RECIPIENT,
                        subject: "AWS Compliance Scan Results - Build #${env.BUILD_NUMBER}",
                        body: """
Hello,

AWS Compliance Scan completed successfully.

==================================================
COMPLIANCE REPORT
==================================================

${reportContent}

==================================================
BUILD DETAILS
==================================================

Build URL:
${env.BUILD_URL}

Report Artifact:
${env.BUILD_URL}artifact/reports/compliance_report.txt

Regards,
Jenkins Automation
"""
                    )

                    echo "Email notification sent."

                } else {

                    mail(
                        to: params.EMAIL_RECIPIENT,
                        subject: "AWS Compliance Scan Failed - Build #${env.BUILD_NUMBER}",
                        body: """
Compliance scan completed but no report file was found.

Build URL:
${env.BUILD_URL}
"""
                    )

                    echo "Report file not found."
                }
            }
        }
    }
}
