import json
from io import BytesIO
from partyfy import partyfy_to_bytes
import base64

def lambda_handler(event, context):
    print("Lambda Event: " + json.dumps(event))

    response = {}

    try:
        gif_in_bytes = grab_gif(event)
        unpartyfied_bytes = BytesIO(gif_in_bytes)
        partyfied_bytes = partyfy_to_bytes(unpartyfied_bytes, 10)
        response["partyfied_gif"] = prep_response(partyfied_bytes)
        response["status"] = "success"
    except Exception as e:
        print("Error: " + str(e))
        response["status"] = "failure"

    return response


def prep_response(partyfied_bytes):
    bytes = partyfied_bytes.read()
    encoded_bytes = base64.encodebytes(bytes)
    return encoded_bytes.decode("utf-8")


def grab_gif(event):
    # make sure it's a gif
    gif_in_bytes = base64.decodestring(bytes(event["body"], "utf-8"))
    return gif_in_bytes
