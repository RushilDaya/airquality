from src.models.aggregratedmeasurement import AggregatedMeasurement

aggregation = AggregatedMeasurement.compute_aggregation("BE_Leuven", "PM10")
aggregation.save()