set KEY_NAME=MyKeyPair
aws ec2 delete-key-pair --key-name %KEY_NAME%
del -f %KEY_NAME%.pem
cdk destroy
