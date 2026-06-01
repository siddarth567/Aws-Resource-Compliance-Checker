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

## Author

**Siddarth**

DevOps / AWS Automation Project

Built as part of hands-on DevOps learning using AWS, Docker, Jenkins and Python.
