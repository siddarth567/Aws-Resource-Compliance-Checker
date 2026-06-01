import boto3
from botocore.exceptions import ClientError

def check_s3_public():

    s3 = boto3.client('s3', region_name='us-east-1')

    results = []

    buckets = s3.list_buckets()

    for bucket in buckets['Buckets']:

        bucket_name = bucket['Name']

        try:

            acl = s3.get_bucket_acl(Bucket=bucket_name)

            for grant in acl['Grants']:

                grantee = grant.get('Grantee', {})

                uri = grantee.get('URI', '')

                if 'AllUsers' in uri:

                    results.append({
                        'Resource': bucket_name,
                        'Issue': 'Public S3 Bucket'
                    })

        except ClientError as e:

            results.append({
                'Resource': bucket_name,
                'Issue': str(e)
            })

    return results
