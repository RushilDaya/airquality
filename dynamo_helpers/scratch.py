from src.aws.dynamodb import DynamoDB
from src.aws import MEASUREMENTS_TABLE

Dynamo = DynamoDB()
response = Dynamo.get_newest_measurement_for_location_param(
    MEASUREMENTS_TABLE,
    "BE_Leuven",
    "CO",
)
print(response)