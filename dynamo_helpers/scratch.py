from src.models.aggregratedmeasurement import AggregatedMeasurement

aggregation = AggregatedMeasurement.compute_aggregation("BE_Leuven", "CO")
aggregation.save()