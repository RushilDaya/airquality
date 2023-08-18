import json
from typing import Optional, Set, Tuple
from src.process_new_aq_measurement import process_new_aq_measurement
from src.update_latest_aggregation import update_latest_aggregation
from src.update_view import update_view

# minimal logic here: just pass the payload to the process_new_aq_measurement function
def lambda_handler(event:dict, context:Optional[dict] = None):
    event_locations_params: Set[Tuple[str,str]] = set()
    for record in event["Records"]:
        print(f"record: {record}")
        payload = record["body"]
        event_location_param = process_new_aq_measurement(payload)
        if event_location_param is not None:
            event_locations_params.add(event_location_param)
    update_latest_aggregation(list(event_locations_params)) # this can be moved to separate function if it gets intensive
    update_view() # this can be moved to separate function if it gets intensive
    return {"statusCode": 200, "body": json.dumps(f'Processed {len(event["Records"])} messages')}


if __name__ == '__main__':
    event = {
        "Records": [
            {
                "body":{
                    "MessageAttributes": {
                        "country" : {"Type":"String","Value":"BE"},
                        "unit" : {"Type":"String","Value":"µg/m³"},
                        "date_utc" : {"Type":"String","Value":"2023-08-14T06:00:00.000Z"},
                        "date_local" : {"Type":"String","Value":"2023-08-14T07:00:00+01:00"},
                        "city" : {"Type":"String","Value":"Leuven"},
                        "sourceType" : {"Type":"String","Value":"government"},
                        "parameter" : {"Type":"String","Value":"pm10"},
                        "latitude" : {"Type":"Number","Value":"50.8823"},
                        "location" : {"Type":"String","Value":"Sluisstraat"},
                        "sourceName" : {"Type":"String","Value":"Leuven"},
                        "value" : {"Type":"Number","Value":"34"},
                        "longitude" : {"Type":"Number","Value":"4.7138"}
                    }
                }
        }
        ]
    }
    response = lambda_handler(event)
    print(response)