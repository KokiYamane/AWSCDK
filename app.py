#!/usr/bin/env python3

from aws_cdk import (
    core,
    aws_ec2 as ec2,
)
import os

# from hello_cdk.hello_cdk_stack import HelloCdkStack

class MyEc2(core.Stack):

    def __init__(self, scope: core.App, name: str, key_name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # <1>
        vpc = ec2.Vpc(
            self, 'MyEc2-Vpc',
            max_azs=1,
            cidr='10.10.0.0/23',
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='public',
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
            nat_gateways=0,
        )

        # <2>
        sg = ec2.SecurityGroup(
            self, 'MyEc2Vpc-Sg',
            vpc=vpc,
            allow_all_outbound=True,
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
        )

        # <3>
        host = ec2.Instance(
            self, 'MyEc2Instance',
            instance_type=ec2.InstanceType('t2.micro'),
            # instance_type=ec2.InstanceType('g4dn.xlarge'),
            machine_image=ec2.MachineImage.generic_linux({
                'ap-northeast-1': 'ami-09c0c16fc46a29ed9'
            }),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=sg,
            key_name=key_name
        )

        # print the server address
        core.CfnOutput(self, 'InstancePublicDnsName', value=host.instance_public_dns_name)
        core.CfnOutput(self, 'InstancePublicIp', value=host.instance_public_ip)


app = core.App()
# HelloCdkStack(app, 'hello-cdk')
MyEc2(
    app, 'MyEc2',
    key_name=app.node.try_get_context('key_name'),
    env={
        'region': os.environ['CDK_DEFAULT_REGION'],
        'account': os.environ['CDK_DEFAULT_ACCOUNT'],
    }
)

app.synth()
