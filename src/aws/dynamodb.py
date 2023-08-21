import boto3
from typing import Optional
from src.config import AWS_PROFILE, AWS_REGION


class DynamoDB:
    def __init__(self):
        boto3_session = boto3.Session(profile_name=AWS_PROFILE)
        self.dynamodb = boto3_session.client("dynamodb", region_name=AWS_REGION)

    @staticmethod
    def to_dynamo_format(data_dict: dict):
        formatted_dict = {}
        for item in data_dict:
            if isinstance(data_dict[item], float):
                formatted_dict[item] = {"N": str(data_dict[item])}
            elif isinstance(data_dict[item], int):
                formatted_dict[item] = {"N": str(data_dict[item])}
            elif isinstance(data_dict[item], str):
                formatted_dict[item] = {"S": data_dict[item]}
            else:
                raise Exception(f"Unknown datatype for: {item}")
        return formatted_dict

    @staticmethod
    def from_dynamo_format(dynamo_dict: dict):
        standard_dict = {}
        for item in dynamo_dict:
            if "N" in dynamo_dict[item]:
                if "." in dynamo_dict[item]["N"]:
                    standard_dict[item] = float(dynamo_dict[item]["N"])
                else:
                    standard_dict[item] = int(dynamo_dict[item]["N"])
            elif "S" in dynamo_dict[item]:
                standard_dict[item] = dynamo_dict[item]["S"]
            else:
                raise Exception(f"Unknown datatype: {dynamo_dict[item]}")
        return standard_dict

    def put_item(self, table_name, data_dict: dict):
        # generic function to put an item into a dynamodb table
        response = self.dynamodb.put_item(TableName=table_name, Item=data_dict)
        print(response)

    def get_all_items(self, table_name: str):
        # this is a full table scan and should only be used for small tables
        response = self.dynamodb.scan(TableName=table_name)
        data = response["Items"]

        while "LastEvaluatedKey" in response:
            response = self.dynamodb.scan(
                TableName=table_name, ExclusiveStartKey=response["LastEvaluatedKey"]
            )
            data.extend(response["Items"])
        return data
    
    def get_filtered_items(self, table_name:str, key_condition_expression:str,
                           expression_attribute_values:dict,
                           filter_expression:Optional[str]=None,
                           scan_forward_index:Optional[bool]=False,
                           limit:Optional[int]=100):
        response = self.dynamodb.query(
            TableName=table_name,
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
            FilterExpression=filter_expression,
            ScanIndexForward=scan_forward_index,
            Limit=limit,
        )
        if response["Count"] == 0:
            return []
        return response["Items"]