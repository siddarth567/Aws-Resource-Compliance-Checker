import boto3

def check_security_groups():

    ec2 = boto3.client('ec2', region_name='us-east-1')

    results = []

    response = ec2.describe_security_groups()

    for sg in response['SecurityGroups']:

        sg_name = sg['GroupName']

        for permission in sg['IpPermissions']:

            from_port = permission.get('FromPort')

            ip_ranges = permission.get('IpRanges', [])

            for ip in ip_ranges:

                cidr = ip.get('CidrIp')

                if cidr == '0.0.0.0/0' and from_port == 22:

                    results.append({
                        'Resource': sg_name,
                        'Issue': 'SSH Open to World'
                    })

    return results
