from src.models.aggregratedmeasurement import AggregatedMeasurement
from src.views.html import create_table_from_aggregations


def update_view():
    # collect all the aggregations
    # recreate the html view file (table)
    # upload the html view file to s3

    # get all the latest aggregations
    aggregations = AggregatedMeasurement.get_all_aggregations()
    html_table = create_table_from_aggregations(aggregations)