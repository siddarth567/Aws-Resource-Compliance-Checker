import boto3

def check_ec2_tags():

    ec2 = boto3.client('ec2', region_name='us-east-1')

    required_tags = ['Owner', 'Environment']

    results = []

    response = ec2.describe_instances()

    for reservation in response['Reservations']:

        for instance in reservation['Instances']:

            instance_id = instance['InstanceId']

            tags = instance.get('Tags', [])

            existing_tags = [tag['Key'] for tag in tags]

            missing_tags = []

            for tag in required_tags:

                if tag not in existing_tags:
                    missing_tags.append(tag)

            if missing_tags:

                results.append({
                    'Resource': instance_id,
                    'Issue': f'Missing Tags: {missing_tags}'
                })

    return results
