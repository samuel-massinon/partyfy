# Partyfy

Convert a gif into a party gif!

## Using

TODO

## Setup

You can use CloudFormation to set up Partyfy on your own AWS account.

First, use `aws cloudformation package` to upload your code
```sh
export AWS_ACCOUNT_ID=(aws sts get-caller-identity --output text --query 'Account')
export PACKAGE_BUCKET="$AWS_ACCOUNT_ID-package-bucket"
aws cloudformation package \
  --template-file cloudformation.yaml \
  --s3-bucket $PACKAGE_BUCKET \
  --output-template-file packaged.yaml
```

Now deploy your stack
```sh
aws cloudformation deploy \
  --template-file /home/sam/invenia/partyfy/packaged.yaml \
  --capabilities CAPABILITY_IAM \
  --stack-name partyfy
```
