import json
from io import BytesIO
from pathlib import posixpath
from partyfy import partyfy_to_bytes
import boto3
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    print("Lambda Event: " + json.dumps(event))

    response = {}

    try:
        gif_in_bytes = grab_gif(event)
        unpartyfied_bytes = BytesIO(gif_in_bytes)
        partyfied_bytes = partyfy_to_bytes(unpartyfied_bytes, 10)
        save_partyfied_gif(partyfied_bytes, event)
        response["status"] = "success"
    except Exception as e:
        print("Error: " + str(e))
        response["status"] = "failure"

    return response


def save_partyfied_gif(partyfied_bytes, event):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = posixpath.join(
        "partyfied",
        posixpath.basename(event["Records"][0]["s3"]["object"]["key"]),
    )
    s3_client.put_object(
        Body=partyfied_bytes,
        Bucket=bucket_name,
        Key=object_key,
    )


def grab_gif(event):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)

    return response["Body"].read()
