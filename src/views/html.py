from typing import List
from src.models.aggregratedmeasurement import AggregatedMeasurement


def create_table_from_aggregations(aggregations: List[AggregatedMeasurement]) -> str:
    print(aggregations)
