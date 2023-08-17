from dataclasses import dataclass
from airqualitymeasurement import AirQualityMeasurement

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

    @classmethod
    def compute_aggregation(cls, composite_location: str, param: str):
        # generator function which will return an AggregatedMeasurement by computing
        # it from latest air quality measurements

        # get the latest measurements
        latest_measurements = AirQualityMeasurement.get_latest_air_quality_measurements(
            composite_location, param, AGGREGATION_WINDOW_HOURS
        )

    def save(self):
        pass
