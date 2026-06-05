# AWS Resource Compliance Checker

## Overview

AWS Resource Compliance Checker is a Python-based automation project that scans AWS resources and identifies non-compliant infrastructure based on predefined security and governance rules.

The project is containerized using Docker and integrated with Jenkins CI/CD to run compliance checks automatically with email and Slack notifications.

---

## Features

* Check EC2 instances for required tags
* Detect public S3 bucket exposure
* Detect Security Groups with SSH open to the world (`0.0.0.0/0`)
* Generate compliance report automatically
* Run inside Docker container
* Trigger scans through Jenkins pipeline
* Archive compliance reports in Jenkins
* **Email notifications** for compliance scan results
* **Slack notifications** for real-time alerts

---

## Project Structure

```bash
aws-compliance-checker/
│
├── checks/
│   ├── ec2_tags.py
│   ├── s3_public.py
│   └── security_groups.py
│
├── reports/
│   └── compliance_report.txt
│
├── main.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
└── README.md
```

---

## Technologies Used

* Python 3
* Boto3
* Docker
* Jenkins
* AWS EC2
* AWS IAM
* GitHub
* Linux (Ubuntu)

---

## Prerequisites

### Install Docker

Docker is required to run the compliance checker and Jenkins. Follow the installation instructions for your operating system:

#### On Ubuntu/Debian

```bash
# Update package index
sudo apt-get update

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify Docker installation
docker --version
docker run hello-world
```

#### On macOS

```bash
# Using Homebrew
brew install docker

# Or download Docker Desktop from https://www.docker.com/products/docker-desktop
# Then run the installer

# Verify installation
docker --version
```

#### On Windows

Download Docker Desktop from: https://www.docker.com/products/docker-desktop

Follow the installer instructions and verify installation:

```bash
docker --version
```

---

### Install Jenkins using Docker

Jenkins can be easily deployed using a Docker container. This approach eliminates the need for manual installation and configuration.

#### Pull Jenkins Docker Image

```bash
docker pull jenkins/jenkins:lts
```

#### Run Jenkins Container

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(which docker):/usr/bin/docker \
  jenkins/jenkins:lts
```

**Parameters explained:**
- `-d`: Run in detached mode (background)
- `--name jenkins`: Container name
- `-p 8080:8080`: Map Jenkins web interface port
- `-p 50000:50000`: Map Jenkins agent port
- `-v jenkins_home:/var/jenkins_home`: Persist Jenkins data
- `-v /var/run/docker.sock:/var/run/docker.sock`: Allow Jenkins to access Docker daemon
- `-v $(which docker):/usr/bin/docker`: Share Docker binary with container

#### Access Jenkins

1. Open your browser and navigate to: `http://localhost:8080`
2. Get the initial admin password:

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

3. Copy the password and paste it into the Jenkins setup wizard
4. Follow the setup wizard to install recommended plugins
5. Create your first admin user

#### Configure Jenkins for Docker Commands

1. Go to **Manage Jenkins** → **System Configuration**
2. Scroll to **Docker** section
3. Add Docker URI: `unix:///var/run/docker.sock`
4. Test the connection

#### Stop/Start Jenkins Container

```bash
# Stop Jenkins
docker stop jenkins

# Start Jenkins
docker start jenkins

# View Jenkins logs
docker logs -f jenkins
```

---

## How to Run Locally

### Clone Repository

```bash
git clone https://github.com/siddarth567/Aws-Resource-Compliance-Checker.git
cd Aws-Resource-Compliance-Checker
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Run Script

```bash
python3 main.py
```

---

## Run with Docker

### Build Docker Image

```bash
docker build -t aws-compliance-checker .
```

### Run Container

```bash
docker run --rm --network host aws-compliance-checker
```

---

## Compliance Checks

### 1. EC2 Tag Compliance Check

Validates whether EC2 instances contain mandatory tags such as:

* Owner
* Environment

Example finding:

```text
i-xxxxxxxxxxxx Missing Tags: Owner, Environment
```

---

### 2. S3 Public Access Check

Checks whether S3 buckets are publicly accessible.

Flags buckets that expose public access unintentionally.

---

### 3. Security Group Check

Scans Security Groups for:

```text
Port 22 open to 0.0.0.0/0
```

Identifies unrestricted SSH access.

Example:

```text
demosecurity → SSH Open to World
```

---

## Jenkins Pipeline

### Pipeline Stages

1. **Checkout Source Code** - Clones the repository
2. **Build Docker Image** - Builds the compliance checker Docker image
3. **Run Compliance Scan** - Executes the compliance scan inside a Docker container
4. **Archive Report** - Archives the compliance report as a Jenkins artifact
5. **Send Slack Notification** - Sends real-time alert to Slack channel
6. **Email Notification** (Post) - Sends detailed compliance report via email

### Trigger

```text
GitHub Push → Jenkins Build → Docker Scan → Compliance Report → Email & Slack Notification
```

### Scheduled Runs

Pipeline runs automatically every day at **8:00 PM UTC** (configurable via cron expression `0 20 * * *`)

---

## Setting up Jenkins Pipeline

### Prerequisites for Notifications

#### Email Setup

1. Go to **Manage Jenkins** → **System Configuration**
2. Scroll to **Email Notification** section
3. Configure your SMTP server:
   - **SMTP server**: `smtp.gmail.com` (or your email provider)
   - **SMTP port**: `587`
   - **User name**: Your email address
   - **Password**: Your email password or app-specific password
   - **SMTP Authentication**: Enable
   - **Use TLS**: Enable
4. Set default recipient email if needed

#### Slack Webhook Setup

1. Go to your Slack workspace settings
2. Create an Incoming Webhook:
   - Navigate to **Apps & Integrations** → **Incoming Webhooks**
   - Click **Create New Webhook**
   - Select the channel to receive notifications
   - Copy the Webhook URL
3. In Jenkins, add the Webhook URL as a secret credential:
   - Go to **Manage Jenkins** → **Manage Credentials**
   - Click **Global credentials**
   - Click **Add Credentials**
   - Kind: **Secret text**
   - Secret: Paste your Slack Webhook URL
   - ID: `SLACK_WEBHOOK`
   - Click **Create**

### Configure Pipeline in Jenkins

1. In Jenkins, click **New Item** → **Pipeline**
2. Enter job name and select **Pipeline**
3. Scroll to **Pipeline** section
4. Select **Pipeline script from SCM**
5. Choose **Git** as SCM
6. Enter repository URL: `https://github.com/siddarth567/Aws-Resource-Compliance-Checker.git`
7. Set script path to: `Jenkinsfile`
8. Configure build triggers:
   - **Poll SCM**: Leave empty (using cron schedule in Jenkinsfile)
   - Or use **GitHub webhook** for real-time triggers
9. Add parameter for EMAIL_RECIPIENT (or use default value)
10. Save and run the pipeline

---

## Email Notification Details

### Recipient Configuration

The email recipient is configurable via Jenkins parameters:
- **Default recipient**: `ksiddharth263@gmail.com`
- **Customizable per build**: Enter email address in build parameters

### Email Content

**Success Notification:**
- Compliance scan status
- Full compliance report content
- Build number and URL
- Link to compliance report artifact

**Failure Notification:**
- Error message indicating missing report file
- Build URL for investigation

### Sample Email

```
Hello,

AWS Compliance Scan completed successfully.

==================================================
COMPLIANCE REPORT
==================================================

Running EC2 Tag Compliance Check...
Running S3 Public Access Check...
Running Security Group Check...

Non-Compliant Resources Found:

i-09ca5ed542aefac1d → Missing Tags: Owner, Environment
demosecurity → SSH Open to World

==================================================
BUILD DETAILS
==================================================

Build URL:
http://jenkins:8080/job/aws-compliance/45/

Report Artifact:
http://jenkins:8080/job/aws-compliance/45/artifact/reports/compliance_report.txt

Regards,
Jenkins Automation
```

---

## Slack Notification Details

### Webhook Configuration

The Slack webhook URL is stored as a Jenkins credential `SLACK_WEBHOOK` for security.

### Notification Message Format

The Slack notification includes:
- 🚨 Alert emoji for visibility
- Job name
- Build number
- Build status
- Direct link to compliance report artifact

### Sample Slack Message

```
🚨 AWS Compliance Scan Completed

Job: AWS-Compliance-Checker
Build: #45
Status: SUCCESS

Report: [View Report](http://jenkins:8080/job/aws-compliance/45/artifact/reports/compliance_report.txt)
```

---

## Sample Output

```text
Running EC2 Tag Compliance Check...
Running S3 Public Access Check...
Running Security Group Check...

Non-Compliant Resources Found:

i-09ca5ed542aefac1d → Missing Tags: Owner, Environment
demosecurity → SSH Open to World
launch-wizard-1 → SSH Open to World
```

---

## Future Enhancements

* Additional checks for:
  * IAM policies
  * EBS encryption
  * RDS backups
  * CloudTrail status
* HTML report generation
* Advanced filtering and reporting
* Custom compliance rules engine
* Dashboard for compliance trends

---

## Troubleshooting

### Docker Issues

**Container fails to build:**
```bash
# Check Docker daemon
sudo systemctl status docker

# Rebuild with verbose output
docker build -t aws-compliance-checker . --verbose
```

### Jenkins Issues

**Cannot connect to Docker:**
- Verify the Docker socket is mounted: `docker exec jenkins ls -la /var/run/docker.sock`
- Ensure Jenkins user has Docker permissions

**Port 8080 already in use:**
```bash
# Change Jenkins port
docker run -d --name jenkins -p 9090:8080 -p 50000:50000 jenkins/jenkins:lts
# Access at http://localhost:9090
```

### Email Notification Issues

**Email not sending:**
- Verify SMTP credentials in Jenkins System Configuration
- Check firewall/port 587 is accessible
- For Gmail: Use app-specific password, not regular password
- Check Jenkins logs: `docker logs -f jenkins`

### Slack Notification Issues

**Webhook returning 404:**
- Verify webhook URL is correct
- Ensure webhook hasn't expired
- Generate a new webhook if needed

**Messages not appearing:**
- Verify the channel exists and bot has permission
- Check Jenkins logs for curl errors
- Confirm webhook URL is stored correctly as secret credential

---

## Author

**Siddarth**

DevOps / AWS Automation Project

Built as part of hands-on DevOps learning using AWS, Docker, Jenkins, Python, with email and Slack integration for automated notifications.
