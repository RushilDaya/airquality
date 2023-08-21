from dataclasses import dataclass
from datetime import datetime

from src.aws.dynamodb import DynamoDB
from src.config import MEASUREMENTS_TABLE
from src import VALIDATION_CONFIGURATION


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
    param: str
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
        dynamodb = DynamoDB()
        dynamo_formatted_values = dynamodb.to_dynamo_format(self.__dict__)
        # add the values which constitute the primary key
        dynamo_formatted_values.update(
            dynamodb.to_dynamo_format({"composite_location": self.composite_location})
        )
        dynamo_formatted_values.update(
            dynamodb.to_dynamo_format({"timestamp_utc": self.timestamp_utc})
        )
        print(f"saving to dynamodb: {dynamo_formatted_values}")
        dynamodb.put_item(MEASUREMENTS_TABLE, dynamo_formatted_values)

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
            param=cls.safeload(raw_measurement, "param", VALIDATION_CONFIGURATION),
            unit=cls.safeload(raw_measurement, "unit", VALIDATION_CONFIGURATION),
            value=cls.safeload(raw_measurement, "value", VALIDATION_CONFIGURATION),
        )

    @classmethod
    def from_dynamo_item(cls, dynamo_item: dict):
        standard_dict = DynamoDB.from_dynamo_format(dynamo_item)
        del standard_dict["composite_location"]  # this is not a property of the class
        del standard_dict["timestamp_utc"]  # this is not a property of the class
        return cls(**standard_dict)

    @classmethod
    def safeload(cls, raw_measurement: dict, key: str, validation_configuration: dict):
        # this validates inputs when ingesting a raw measurement for the first time
        # it is not used when querying the database (assumes data is already validated)

        if key == "param":
            # param is a special case because it is a reserved keyword in dynamodb
            # need to extract it as param instead of parameter
            # Find a more elegant solution for this
            value = raw_measurement["MessageAttributes"]["parameter"]["Value"]
        else:
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

    @classmethod
    def get_latest_air_quality_measurements(
        cls, composite_location: str, param: str, window_hours: int
    ):
        # gathers all the latest measurements for a given composite location and param
        # going back a given number of hours from the latest measurement
        # returns a list of AirQualityMeasurement objects
        dynamodb = DynamoDB()
        measurement = dynamodb.get_newest_measurement_for_location_param(
            MEASUREMENTS_TABLE, composite_location, param
        )
        latest_timestamp_epoch = int(measurement["timestamp_utc"]["N"])
        start_time = latest_timestamp_epoch - 3600 * window_hours
        measurements = dynamodb.get_measurements_from(
            MEASUREMENTS_TABLE, composite_location, param, start_time
        )
        return [cls.from_dynamo_item(item) for item in measurements]


# we need to keep the dynamo stuff generic
class InvalidAirQualityMeasurement(Exception):
    pass
