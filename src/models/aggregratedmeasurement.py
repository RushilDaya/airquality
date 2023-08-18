from dataclasses import dataclass
from src.aws.dynamodb import DynamoDB
from src.aws import AGGREGATIONS_TABLE
from src.models.airqualitymeasurement import AirQualityMeasurement

AGGREGATION_WINDOW_HOURS = 3


@dataclass
class AggregatedMeasurement:
    country: str
    city: str
    approximate_longitude: float
    approximate_latitude: float
    param: str
    unit: str
    aggregated_value: float
    lastest_measurement_time_utc: str
    lastest_measurement_time_local: str
    lastest_measurement_time_epoch: int
    aggregation_window_hours: int
    number_of_measurements_in_window: int

    # see if there is an easier way to do this
    # can it be taken from the dataclass?
    datatypes = {
        "country": "str",
        "city": "str",
        "approximate_longitude": "float",
        "approximate_latitude": "float",
        "param": "str",
        "unit": "str",
        "aggregated_value": "float",
        "lastest_measurement_time_utc": "str",
        "lastest_measurement_time_local": "str",
        "lastest_measurement_time_epoch": "int",
        "aggregation_window_hours": "int",
        "number_of_measurements_in_window": "int",
    }

    @property
    def composite_location(self) -> str:
        return f"{self.country}_{self.city}"

    @classmethod
    def compute_aggregation(cls, composite_location: str, param: str):
        # generator function which will return an AggregatedMeasurement by computing
        # it from latest air quality measurements

        # get the latest measurements
        latest_measurements = AirQualityMeasurement.get_latest_air_quality_measurements(
            composite_location, param, AGGREGATION_WINDOW_HOURS
        )
        if len(latest_measurements) == 0:
            return None

        if len(set([measurement.unit for measurement in latest_measurements])) > 1:
            raise ValueError("multiple units for same param - unit conversion not implemented")

        approximate_longitude = sum(
            [measurement.longitude for measurement in latest_measurements]
        ) / len(latest_measurements)
        approximate_latitude = sum(
            [measurement.latitude for measurement in latest_measurements]
        ) / len(latest_measurements)
        aggregated_value = sum([measurement.value for measurement in latest_measurements]) / len(
            latest_measurements
        )

        latest_measurements.sort(key=lambda x: x.timestamp_utc, reverse=True)
        latest_measurement = latest_measurements[0]

        return cls(
            country=latest_measurement.country,
            city=latest_measurement.city,
            approximate_longitude=approximate_longitude,
            approximate_latitude=approximate_latitude,
            param=latest_measurement.param,
            unit=latest_measurement.unit,
            aggregated_value=aggregated_value,
            lastest_measurement_time_utc=latest_measurement.date_utc,
            lastest_measurement_time_local=latest_measurement.date_local,
            lastest_measurement_time_epoch=latest_measurement.timestamp_utc,
            aggregation_window_hours=AGGREGATION_WINDOW_HOURS,
            number_of_measurements_in_window=len(latest_measurements),
        )

    def save(self):
        # save to dynamodb table
        dynamodb = DynamoDB()

        data_dict = self.__dict__
        dynamo_formatted_values = dynamodb.format_values(data_dict, self.datatypes)
        # add the values which constitute the primary key
        dynamo_formatted_values.update(
            dynamodb.format_values(
                {"composite_location": self.composite_location}, {"composite_location": "str"}
            )
        )
        print(f"saving to dynamodb: {dynamo_formatted_values}")
        dynamodb.put_item(AGGREGATIONS_TABLE, dynamo_formatted_values)

    @classmethod
    def get_all_aggregations(cls):
        # get all the aggregations from dynamodb
        dynamodb = DynamoDB()
        aggregations = dynamodb.get_all_items(AGGREGATIONS_TABLE)
        # removev the composite_location from the dict
        for aggregation in aggregations:
            del aggregation["composite_location"]
        formatted = [
            dynamodb.from_dynamo_to_standard_dict(aggregation, cls.datatypes)
            for aggregation in aggregations
        ]
        return [cls(**formatted_agg) for formatted_agg in formatted]
