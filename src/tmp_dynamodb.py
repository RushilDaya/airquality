# attempting to connect to dynamodb scratch pad to be refined later on

import boto3

boto3_session = boto3.Session(profile_name='dataminded')
dynamodb = boto3_session.client('dynamodb', region_name='eu-west-1')

response = dynamodb.query(
    TableName='airmax-rushildaya-aq-measurements',
    KeyConditionExpression='composite_location = :composite_location',
    ExpressionAttributeValues={
        ':composite_location':{'S':'BE_Dinant'},
    },
    ConsistentRead=True,
    ReturnConsumedCapacity='TOTAL'
)
print(response)