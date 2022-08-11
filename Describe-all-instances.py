#This srcipt for describing information about all EC2 and attached volumes.
import boto3

def describe_all_instances():
    ec2client = boto3.client("ec2")
    ec2volumes = ec2client.describe_volumes()
    my_instances = []
    paginator = ec2client.get_paginator('describe_instances')
    pages = paginator.paginate(
        PaginationConfig={
            'MaxItems': 1000,
            'PageSize': 1000
        }
    )

    count = 0
    countrun = 0

    for page in pages:
     reservations = page['Reservations']
     for reservation in reservations:
            instances = reservation['Instances']
            for instance in instances:
                instance_id = instance['InstanceId']
                instance_tags = instance['Tags']
                instance_ip = instance['PrivateIpAddress']
                instance_platform = instance['PlatformDetails']
                instance_type = instance['InstanceType']
                instance_state = instance['State']['Name']
                if instance_state == "running": countrun = countrun+1
                instance_name = "None"
                for tag in instance_tags:
                    if tag['Key'] == "Name":
                        instance_name = tag['Value']
                        break
                my_instances.append(
                    {
                        "instance_id": instance_id,
                        "instance_name": instance_name,
                        "instance_ip": instance_ip,
                        "instance_platfrom": instance_platform,
                        "instance_type": instance_type,
                        "instance_state": instance_state
                    }
                )

                print(instance_id,instance_name,instance_type,instance_platform,instance_ip,instance_state)

                for disk in ec2volumes['Volumes']:
                         for attachments in disk['Attachments']:
                            if attachments['InstanceId'] == instance_id:
                                print(disk['VolumeId'], disk['VolumeType'], disk['Size'])

    print("You have:", len(my_instances),"instances and ", countrun, "running instances")
    return my_instances


describe_all_instances()
