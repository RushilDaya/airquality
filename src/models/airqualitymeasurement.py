from dataclasses import dataclass
import json
from datetime import datetime

from src.aws.dynamodb import DynamoDB

VALIDATION_CONFIGURATION = json.load(open("src/models/validators/airqualitymeasurement.json"))


@dataclass
class AirQualityMeasurement:
    country: str
    city: str
    location: str
    latitude: float
    longitude: float
    sourceName: str
    sourceType: str
    date_utc: str
    date_local: str
    parameter: str
    unit: str
    value: float

    @property
    def composite_location(self) -> str:
        return f"{self.country}_{self.city}"

    @property
    def timestamp_utc(self) -> int:
        # timestamp in epoch format
        return int(datetime.strptime(self.date_utc, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())

    def save(self):
        # save to dynamodb table
        datatypes = {k: v["type"] for k, v in VALIDATION_CONFIGURATION.items()}
        dynamodb = DynamoDB()
        dynamo_formatted_values = dynamodb.format_values(self.__dict__, datatypes)
        # add the values which constitute the primary key
        dynamo_formatted_values.update(
            dynamodb.format_values(
                {"composite_location": self.composite_location}, {"composite_location": "str"}
            )
        )
        dynamo_formatted_values.update(
            dynamodb.format_values({"timestamp_utc": self.timestamp_utc}, {"timestamp_utc": "int"})
        )
        print(f"saving to dynamodb: {dynamo_formatted_values}")
        dynamodb.put_measurement(dynamo_formatted_values)

    @classmethod
    def from_raw_message(cls, raw_measurement: dict):
        return cls(
            country=cls.safeload(raw_measurement, "country", VALIDATION_CONFIGURATION),
            city=cls.safeload(raw_measurement, "city", VALIDATION_CONFIGURATION),
            location=cls.safeload(raw_measurement, "location", VALIDATION_CONFIGURATION),
            latitude=cls.safeload(raw_measurement, "latitude", VALIDATION_CONFIGURATION),
            longitude=cls.safeload(raw_measurement, "longitude", VALIDATION_CONFIGURATION),
            sourceName=cls.safeload(raw_measurement, "sourceName", VALIDATION_CONFIGURATION),
            sourceType=cls.safeload(raw_measurement, "sourceType", VALIDATION_CONFIGURATION),
            date_utc=cls.safeload(raw_measurement, "date_utc", VALIDATION_CONFIGURATION),
            date_local=cls.safeload(raw_measurement, "date_local", VALIDATION_CONFIGURATION),
            parameter=cls.safeload(raw_measurement, "parameter", VALIDATION_CONFIGURATION),
            unit=cls.safeload(raw_measurement, "unit", VALIDATION_CONFIGURATION),
            value=cls.safeload(raw_measurement, "value", VALIDATION_CONFIGURATION),
        )

    @classmethod
    def safeload(cls, raw_measurement: dict, key: str, validation_configuration: dict):
        # this validates inputs when ingesting a raw measurement for the first time
        # it is not used when querying the database (assumes data is already validated)
        value = raw_measurement["MessageAttributes"][key]["Value"]
        if validation_configuration.get(key) is None:
            raise InvalidAirQualityMeasurement(f"Unkown key: {key}")

        # force type conversion
        if validation_configuration[key]["type"] == "float":
            value = float(value)
        if validation_configuration[key]["type"] == "int":
            value = int(value)
        if validation_configuration[key]["type"] == "str":
            value = str(value)

        # force case conversion
        if validation_configuration[key].get("case") is not None:
            if validation_configuration[key]["case"] == "upper":
                value = value.upper()
            if validation_configuration[key]["case"] == "lower":
                value = value.lower()

        # check accepted values
        if validation_configuration[key].get("accepted_values") is not None:
            if value not in validation_configuration[key]["accepted_values"]:
                raise InvalidAirQualityMeasurement(f"Invalid value for {key}: {value}")

        # check accepted ranges
        if validation_configuration[key].get("accepted_range") is not None:
            if (
                value < validation_configuration[key]["accepted_range"]["min"]
                or value > validation_configuration[key]["accepted_range"]["max"]
            ):
                raise InvalidAirQualityMeasurement(f"Invalid value for {key}: {value}")
        return value


class InvalidAirQualityMeasurement(Exception):
    pass
