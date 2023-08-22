# when running this code will randomly generate
# a data point every X seconds and send it to the SQS queue.
# these data points should mimick what we consider to be
# a valid data point in the openaq project.

SQS_QUEUE_URL = "https://sqs.eu-west-1.amazonaws.com/287820185021/openaq-rushildaya-mock-loader"
AWS_PROFILE = "dataminded"
AWS_REGION = "eu-west-1"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"
DATE_FORMAT_LOCAL = "%Y-%m-%dT%H:%M:%S%z"
OFFSET_HOURS = 1
VALUE_MIN = 0.0
VALUE_MAX = 50.0
INTERVAL_SECONDS = 5

import time
import json
import random
import boto3

Locations = [
    {
        "country": {"Type": "String", "Value": "BE"},
        "city": {"Type": "String", "Value": "Leuven"},
        "sourceType": {"Type": "String", "Value": "government"},
        "latitude": {"Type": "Number", "Value": "51.8823"},
        "location": {"Type": "String", "Value": "Sluisstraat"},
        "sourceName": {"Type": "String", "Value": "Leuven"},
        "longitude": {"Type": "Number", "Value": "4.7138"},
    },
    {
        "country": {"Type": "String", "Value": "BE"},
        "city": {"Type": "String", "Value": "Antwerp"},
        "sourceType": {"Type": "String", "Value": "government"},
        "latitude": {"Type": "Number", "Value": "51.2213"},
        "location": {"Type": "String", "Value": "Catherdral"},
        "sourceName": {"Type": "String", "Value": "Antwerp"},
        "longitude": {"Type": "Number", "Value": "4.4051"},
    },
    {
        "country": {"Type": "String", "Value": "BE"},
        "city": {"Type": "String", "Value": "Brussels"},
        "sourceType": {"Type": "String", "Value": "government"},
        "latitude": {"Type": "Number", "Value": "50.84476"},
        "location": {"Type": "String", "Value": "Atomium"},
        "sourceName": {"Type": "String", "Value": "Brussels"},
        "longitude": {"Type": "Number", "Value": "4.3572"},
    },
    {
        "country": {"Type": "String", "Value": "BE"},
        "city": {"Type": "String", "Value": "Liege"},
        "sourceType": {"Type": "String", "Value": "government"},
        "latitude": {"Type": "Number", "Value": "50.6330"},
        "location": {"Type": "String", "Value": "montagne de bueren"},
        "sourceName": {"Type": "String", "Value": "Liege"},
        "longitude": {"Type": "Number", "Value": "5.5697"},
    },
]

parameters = [
    {
        "unit": {"Type": "String", "Value": "µg/m³"},
        "parameter": {"Type": "String", "Value": "pm10"},
    },
    {
        "unit": {"Type": "String", "Value": "ppb"},
        "parameter": {"Type": "String", "Value": "O₃"},
    },
    {
        "unit": {"Type": "String", "Value": "ppm"},
        "parameter": {"Type": "String", "Value": "CO"},
    },
    {
        "unit": {"Type": "String", "Value": "ppb"},
        "parameter": {"Type": "String", "Value": "NO₂"},
    },
]


def data_generator():
    random.seed()
    while True:
        data_point = {}
        location = random.choice(Locations)
        parameter = random.choice(parameters)
        data_point.update(location)
        data_point.update(parameter)
        data_point["value"] = {"Type": "Number", "Value": str(random.uniform(VALUE_MIN, VALUE_MAX))}

        # generate a timestamp
        timestamp = time.time()
        data_point["date_utc"] = {
            "Type": "String",
            "Value": time.strftime(DATE_FORMAT, time.gmtime(timestamp)),
        }
        data_point["date_local"] = {
            "Type": "String",
            "Value": time.strftime(DATE_FORMAT_LOCAL, time.localtime(timestamp)),
        }
        yield data_point


if __name__ == "__main__":
    aws_session = boto3.Session(profile_name=AWS_PROFILE)
    sqs = aws_session.client("sqs", region_name=AWS_REGION)

    generator = data_generator()
    while True:
        data_point = next(generator)
        data_point = {"MessageAttributes": data_point}
        print(data_point)
        sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(data_point))
        time.sleep(INTERVAL_SECONDS)
