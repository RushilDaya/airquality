import boto3
import json

SQS_QUEUE_URL = "https://sqs.eu-west-1.amazonaws.com/287820185021/openaq-rushildaya-mock-loader"
MOCK_DATA_SOURCE = "mock_data/mock_data.json"

def send_mock_data_to_sqs():
    aws_session = boto3.Session(profile_name="dataminded")
    sqs = aws_session.client("sqs", region_name="eu-west-1")
    with open(MOCK_DATA_SOURCE, "r") as f:
        mock_data = json.load(f)
    for record in mock_data['mock_data']:
        sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(record))

if __name__ == '__main__':
    send_mock_data_to_sqs()