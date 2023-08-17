import boto3
from src.aws import PROFILE, REGION


class DynamoDB:
    def __init__(self):
        boto3_session = boto3.Session(profile_name=PROFILE)
        self.dynamodb = boto3_session.client("dynamodb", region_name=REGION)

    @staticmethod
    def format_values(data_dict: dict, datatypes: dict):
        formatted_dict = {}
        for item in data_dict:
            if datatypes[item] == "float":
                formatted_dict[item] = {"N": str(data_dict[item])}
            elif datatypes[item] == "int":
                formatted_dict[item] = {"N": str(data_dict[item])}
            elif datatypes[item] == "str":
                formatted_dict[item] = {"S": data_dict[item]}
            else:
                raise Exception(f"Unknown datatype: {datatypes[item]}")
        return formatted_dict
    
    @staticmethod
    def from_dynamo_to_standard_dict(dynamo_dict: dict):
        standard_dict = {}
        for item in dynamo_dict:
            if "N" in dynamo_dict[item]:
                standard_dict[item] = float(dynamo_dict[item]["N"])
            elif "S" in dynamo_dict[item]:
                standard_dict[item] = dynamo_dict[item]["S"]
            else:
                raise Exception(f"Unknown datatype: {dynamo_dict[item]}")
        return standard_dict

    def put_item(self, table_name, data_dict: dict):
        # generic function to put an item into a dynamodb table
        response = self.dynamodb.put_item(TableName=table_name, Item=data_dict)
        print(response)

    def get_newest_measurement_for_location_param(
        self, table_name: str, composite_location: str, param: str
    ):
        # this function is very specific should be refactored so there
        # is no model specific logic in this dynamodb class if there is time
        response = self.dynamodb.query(
            TableName=table_name,
            KeyConditionExpression="composite_location = :composite_location",
            ExpressionAttributeValues={
                ":composite_location": {"S": composite_location},
                ":param": {"S": param},
            },
            FilterExpression="param = :param",
            ScanIndexForward=False,
            Limit=1,
        )
        if response["Count"] == 0:
            return []
        return response["Items"][0]
    
    def get_measurements_from(
        self, table_name: str, composite_location: str, param: str, start_time_epoch: int
    ):
        # this function is very specific should be refactored so there
        # is no model specific logic in this dynamodb class if there is time
        response = self.dynamodb.query(
            TableName=table_name,
            KeyConditionExpression="composite_location = :composite_location AND timestamp_utc >= :timestamp_utc",
            ExpressionAttributeValues={
                ":composite_location": {"S": composite_location},
                ":param": {"S": param},
                ":timestamp_utc": {"N": str(start_time_epoch)},
            },
            FilterExpression="param = :param",
            ScanIndexForward=False,
            Limit=200,
        )
        if response["Count"] == 0:
            return []
        return response["Items"]
    
