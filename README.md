# AWS Resource Compliance Checker

## Overview

AWS Resource Compliance Checker is a Python-based automation project that scans AWS resources and identifies non-compliant infrastructure based on predefined security and governance rules.

The project is containerized using Docker and integrated with Jenkins CI/CD to run compliance checks automatically.

---

## Features

* Check EC2 instances for required tags
* Detect public S3 bucket exposure
* Detect Security Groups with SSH open to the world (`0.0.0.0/0`)
* Generate compliance report automatically
* Run inside Docker container
* Trigger scans through Jenkins pipeline
* Archive compliance reports in Jenkins

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

# Install Docker dependencies
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update package index
sudo apt-get update

# Install Docker Engine
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Add your user to the docker group (optional, to run docker without sudo)
sudo usermod -aG docker $USER
newgrp docker

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

Pipeline stages:

* Checkout Source Code
* Build Docker Image
* Run AWS Compliance Scan
* Archive Compliance Report

Trigger:

```text
GitHub Push → Jenkins Build → Docker Scan → Compliance Report
```

### Setting up Jenkins Pipeline

1. In Jenkins, click **New Item** → **Pipeline**
2. Configure your GitHub repository URL
3. Set the Pipeline script path to: `Jenkinsfile`
4. Configure build triggers (e.g., GitHub webhook or poll SCM)
5. Save and run the pipeline

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

* Email alerts for failed compliance checks
* Slack notifications
* HTML report generation
* Scheduled scans using Jenkins cron jobs
* Additional checks for:

  * IAM policies
  * EBS encryption
  * RDS backups
  * CloudTrail status

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

---

## Author

**Siddarth**

DevOps / AWS Automation Project

Built as part of hands-on DevOps learning using AWS, Docker, Jenkins and Python.
