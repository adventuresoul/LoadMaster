import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS')
aws_secret_access_key = os.getenv('AWS_SECRET')
region_name = os.getenv('AWS_REGION')

# create an EC2 client
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

instance_type = os.getenv('INSTANCE_TYPE')
key_name = os.getenv('KEY_NAME')
security_group_id = [os.getenv('SECURITY_GROUP_ID')]
subnet_id = os.getenv('SUBNET_ID')
image_id = os.getenv('IMAGE_ID')

# with open("vm_configure.sh", "r") as file:
#     user_data = file.read()



response = ec2_client.run_instances(
    ImageId=image_id,
    InstanceType=instance_type,
    KeyName=key_name,
    SecurityGroupIds=security_group_id, 
    SubnetId=subnet_id, 
    MinCount=1,
    MaxCount=1
)

# Get the instance ID
instance_id = response['Instances'][0]['InstanceId']

# Wait for the instance to reach a running state
waiter = ec2_client.get_waiter('instance_running')
waiter.wait(InstanceIds=[instance_id])

print(f"Instance created with ID: {instance_id}")
