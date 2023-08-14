from dataclasses import dataclass
import json


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

    def save(self):
        # save to dynamodb table
        print(f"Saving measurement: {self.__dict__}")

    @classmethod
    def from_raw_message(cls, raw_measurement: dict):
        validation_configuration = json.load(
            open("src/models/validators/airqualitymeasurement.json")
        )
        return cls(
            country=cls.safeload(raw_measurement, "country", validation_configuration),
            city=cls.safeload(raw_measurement, "city", validation_configuration),
            location=cls.safeload(raw_measurement, "location", validation_configuration),
            latitude=cls.safeload(raw_measurement, "latitude", validation_configuration),
            longitude=cls.safeload(raw_measurement, "longitude", validation_configuration),
            sourceName=cls.safeload(raw_measurement, "sourceName", validation_configuration),
            sourceType=cls.safeload(raw_measurement, "sourceType", validation_configuration),
            date_utc=cls.safeload(raw_measurement, "date_utc", validation_configuration),
            date_local=cls.safeload(raw_measurement, "date_local", validation_configuration),
            parameter=cls.safeload(raw_measurement, "parameter", validation_configuration),
            unit=cls.safeload(raw_measurement, "unit", validation_configuration),
            value=cls.safeload(raw_measurement, "value", validation_configuration),
        )

    @classmethod
    def safeload(cls, raw_measurement: dict, key: str, validation_configuration: dict):
        # this validates inputs when ingesting a raw measurement for the first time
        # it is not used when querying the database (assumes data is already validated)
        value = raw_measurement["MessageAttributes"][key]["Value"]
        if validation_configuration.get(key) is None:
            return value

        # force type conversion
        if validation_configuration[key]["type"] == "float":
            value = float(value)
        if validation_configuration[key]["type"] == "int":
            value = int(value)
        if validation_configuration[key]["type"] == "str":
            value = str(value)

        #force case conversion
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
