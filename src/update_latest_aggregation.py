from typing import List, Tuple

def update_latest_aggregation(locations_params_updated: List[Tuple[str, str]]) -> None:
    # function will gather all the measurements for a given location key and param
    # and then update the latest aggregation table for that location and param
    # the aggregation does not look at the last X hours
    # but rather the last X hours centered around the  latest measurement and then the 
    # last update time is also stored

    for location_param in locations_params_updated:
        print(f"updating latest aggregation for {location_param}")




