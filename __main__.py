import pulumi
import pulumi_aws as aws
from pulumi_aws import ec2

# AMI image configuration
ec2_image_id = 'ami-0cc0a36f626a4fdf5'
ec2_image_owner = '099720109477'
ec2_instance_size = 't2.micro'
ec2_instance_name = 'aws-ec2-ubuntu'

# Lets use Pulumi to get the AMI image
pulumi_ami = aws.get_ami(
                    filters = [{ "name": "image-id", "values": [ec2_image_id]}],
                    owners  = [ec2_image_owner])

# Create a EC2 security group
ssh_port = 22

pulumi_security_group = ec2.SecurityGroup(
                            'pulumi-secgrp',
                            description = 'Enable HTTP access',
                            ingress = [
                                { 'protocol': 'tcp', 'from_port': ssh_port, 'to_port': ssh_port, 'cidr_blocks': ['0.0.0.0/0'] }
                            ]
)

# Create EC2 instance
ec2_instance = ec2.Instance(
                    ec2_instance_name,
                    instance_type = ec2_instance_size,
                    security_groups = [pulumi_security_group.name],
                    ami = pulumi_ami.id
)

pulumi.export('publicIp', ec2_instance.public_ip)
pulumi.export('publicHostName', ec2_instance.public_dns)
