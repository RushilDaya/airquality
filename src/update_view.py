from src.models.aggregratedmeasurement import AggregatedMeasurement
from src.views.html import create_tables_from_aggregations, create_full_page
from src.aws.s3 import upload_file_to_s3
from src.config import S3_VIEW_BUCKET


def update_view():
    # collect all the aggregations
    # recreate the html view file (table)
    # upload the html view file to s3

    aggregations = AggregatedMeasurement.get_all_aggregations()
    html_tables = create_tables_from_aggregations(aggregations)
    full_page = create_full_page(html_tables)
    response = upload_file_to_s3(S3_VIEW_BUCKET, full_page, "index.html")
    print(response)
