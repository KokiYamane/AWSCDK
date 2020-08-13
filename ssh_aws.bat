set KEY_NAME=MyKeyPair
ssh -i %KEY_NAME%.pem -L localhost:8931:localhost:8888 ec2-user@%1
