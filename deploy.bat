set KEY_NAME=MyKeyPair
aws ec2 create-key-pair --key-name %KEY_NAME% --query "KeyMaterial" --output text > %KEY_NAME%.pem
cdk deploy -c key_name=%KEY_NAME%
