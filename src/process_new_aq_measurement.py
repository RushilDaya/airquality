import json
from typing import Tuple
from src.models.airqualitymeasurement import AirQualityMeasurement


def process_new_aq_measurement(raw_measurement: dict) -> Tuple[str, str]:
    """
    function will parse the incoming air quality measurement,
    validate that it has a correct structure,
    and then store the values  to a table
    """
    print(f"raw measurement: {raw_measurement}")

    # if the raw message is  a string, convert it to a dict
    if isinstance(raw_measurement, str):
        print("converting raw measurement to dict")
        raw_measurement = json.loads(raw_measurement)

    measurement = AirQualityMeasurement.from_raw_message(raw_measurement)
    measurement.save()

    return measurement.composite_location, measurement.param
