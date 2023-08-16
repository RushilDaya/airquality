from src.models.airqualitymeasurement import AirQualityMeasurement, InvalidAirQualityMeasurement

def process_new_aq_measurement(raw_measurement: dict):
    """
    function will parse the incoming air quality measurement,
    validate that it has a correct structure,
    and then store the values  to a table
    """
    print(f"raw measurement: {raw_measurement}")
    measurement = AirQualityMeasurement.from_raw_message(raw_measurement)
    measurement.save()
    
    
