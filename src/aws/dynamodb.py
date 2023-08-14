import boto3
from src.aws import PROFILE, REGION, MEASUREMENTS_TABLE


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

    def put_measurement(self, data_dict: dict):
        # need to define the function which will put measurements to dynamodb
        response = self.dynamodb.put_item(TableName=MEASUREMENTS_TABLE, Item=data_dict)
        print(response)
