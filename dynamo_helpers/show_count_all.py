import boto3

boto3_session = boto3.Session(profile_name='dataminded')
dynamodb = boto3_session.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('airmax-rushildaya-aq-measurements')

response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
    
print(data)
print(f"count measurements: {len(data)}")

table = dynamodb.Table('airmax-rushildaya-aq-aggregations')

response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
    
print(data)
print(f"count aggregations: {len(data)}")