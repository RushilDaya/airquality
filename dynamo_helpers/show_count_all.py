import boto3
from src.config import (
    AWS_PROFILE,
    AWS_REGION,
    MEASUREMENTS_TABLE,
    AGGREGATIONS_TABLE
)

boto3_session = boto3.Session(profile_name=AWS_PROFILE)
dynamodb = boto3_session.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(MEASUREMENTS_TABLE)

response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
    
print(data)
print(f"count measurements: {len(data)}")

table = dynamodb.Table(AGGREGATIONS_TABLE)

response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
    
print(data)
print(f"count aggregations: {len(data)}")