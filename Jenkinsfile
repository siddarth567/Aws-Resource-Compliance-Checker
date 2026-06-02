pipeline {
    agent any

    triggers {
        cron('0 20 * * *')
    }

    parameters {
        string(name: 'EMAIL_RECIPIENT', defaultValue: 'ksiddharth263@gmail.com', description: 'Email address to send the compliance report to')
    }

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

    post {
        always {
            script {
                try {
                    // Check if file exists before trying to read and email
                    if (fileExists('reports/compliance_report.txt')) {
                        def reportContent = readFile 'reports/compliance_report.txt'
                        def recipient = params.EMAIL_RECIPIENT ?: 'ksiddharth263@gmail.com'
                        emailext (
                            subject: "AWS Compliance Scan Results - Build #${env.BUILD_NUMBER}",
                            body: "Hello,\n\nHere are the latest AWS resource compliance scan results:\n\n${reportContent}\n\nFor more details, check the Jenkins build link: ${env.BUILD_URL}",
                            to: recipient,
                            attachmentsPattern: 'reports/compliance_report.txt'
                        )
                    } else {
                        echo "No compliance report file found to email."
                    }
                } catch (Exception e1) {
                    echo "emailext failed: ${e1.message}. Trying standard mail step..."
                    try {
                        if (fileExists('reports/compliance_report.txt')) {
                            def reportContent = readFile 'reports/compliance_report.txt'
                            def recipient = params.EMAIL_RECIPIENT ?: 'ksiddharth263@gmail.com'
                            mail (
                                to: recipient,
                                subject: "AWS Compliance Scan Results - Build #${env.BUILD_NUMBER}",
                                body: "Hello,\n\nHere are the latest AWS resource compliance scan results:\n\n${reportContent}\n\nFor more details, check the Jenkins build link: ${env.BUILD_URL}"
                            )
                        }
                    } catch (Exception e2) {
                        echo "Standard mail step also failed: ${e2.message}."
                        echo "Please verify that the Jenkins Mailer / Email Extension plugin is installed and the SMTP server is configured in System Settings."
                    }
                }
            }
        }
    }
}
