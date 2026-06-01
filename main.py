from checks.ec2_tags import check_ec2_tags
from checks.s3_public import check_s3_public
from checks.security_groups import check_security_groups

from tabulate import tabulate

all_results = []

print("\nRunning EC2 Tag Compliance Check...")
all_results.extend(check_ec2_tags())

print("Running S3 Public Access Check...")
all_results.extend(check_s3_public())

print("Running Security Group Check...")
all_results.extend(check_security_groups())

if all_results:

    print("\nNon-Compliant Resources Found:\n")

    print(tabulate(all_results, headers="keys", tablefmt="grid"))

else:

    print("\nAll Resources are Compliant.")

import os
from tabulate import tabulate

# Create reports folder if not present
os.makedirs("reports", exist_ok=True)

# Save report
with open("reports/compliance_report.txt", "w") as f:
    f.write(tabulate(all_results, headers="keys", tablefmt="grid"))

print("Report saved to reports/compliance_report.txt")
