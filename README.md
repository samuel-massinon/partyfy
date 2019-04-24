# Partyfy

Convert a gif into a party gif!


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
  --template-file packaged.yaml \
  --capabilities CAPABILITY_IAM \
  --stack-name partyfy
```

## Using

Let's upload a GIF from CLI

```sh
export BUCKET_NAME=(
  aws cloudformation describe-stacks \
    --stack-name partyfy \
    --output text \
    --query "Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue"
)
```
or if you want to cheat
```sh
export BUCKET_NAME=$AWS_ACCOUNT_ID-partyfy
```
Upload a file to S3 (`blob-octopus.gif` in this example)
```sh
aws s3 cp blob-octopus.gif  s3://$BUCKET_NAME/prepartyfy/
```
Check that your file is on S3, or if your GIF has been partyfied
```sh
aws s3 ls s3://$BUCKET_NAME --recursive
```
Download partyfied GIF. (`blob-octopus.gif` in this example)
```sh
aws s3 cp s3://$BUCKET_NAME/partyfied/blob-octopus.gif ~/Downloads/
```
