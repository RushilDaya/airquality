from pytest import fixture
import json
from typing import List
from src.process_new_aq_measurement import process_new_aq_measurement
from src.models.airqualitymeasurement import AirQualityMeasurement

def load_measurements(path: str) -> List[dict]:
    with open(path, 'r') as f:
        return json.load(f)["measurements"]
    

@fixture(params=load_measurements('tests/resources/valid_measurements.json'))
def valid_measurement_dict(request):
    # parametrized fixture that will load the valid measurements
    return request.param


def test_process_valid_measurements(valid_measurement_dict, monkeypatch):
    # this test is a bit silly, but valids end to end flow
    # of the process measurement function in the happy path

    def monkey_save(self):
        print("monkeypatched save method")
        pass
    monkeypatch.setattr(AirQualityMeasurement, "save", monkey_save)

    location, parameter = process_new_aq_measurement(valid_measurement_dict)
    assert type(location) == str
    assert type(parameter) == str
    assert False