from typing import List, Tuple
from src.models.aggregratedmeasurement import AggregatedMeasurement


def update_latest_aggregation(locations_params_updated: List[Tuple[str, str]]) -> None:
    # function will gather all the measurements for a given location key and param
    # and then update the latest aggregation table for that location and param
    # the aggregation does not look at the last X hours
    # but rather the last X hours centered around the  latest measurement and then the
    # last update time is also stored

    for location_param in locations_params_updated:
        print(f"attempting to update aggregation for {location_param[0]} {location_param[1]}")
        aggregation = AggregatedMeasurement.compute_aggregation(
            location_param[0], location_param[1]
        )
        if aggregation is not None:
            print(f"updating aggregation for {location_param[0]} {location_param[1]}")
            print(aggregation.__dict__)
            aggregation.save()
