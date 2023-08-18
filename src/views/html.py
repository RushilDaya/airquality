from typing import List
from src.models.aggregratedmeasurement import AggregatedMeasurement

def create_full_page(html_elements: List[str]) -> str:
    # return a full html page with the given html elements
    # inserted into the body in the order they appear in the list
    return f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <title>Latest Air Quality Measurements</title>
                <style>
                    table, th, td {{
                        border: 1px solid black;
                        border-collapse: collapse;
                    }}
                    th, td {{
                        padding: 5px;
                        text-align: left;
                    }}
                </style>
            </head>
            <body>
                {"".join(html_elements)}
            </body>
        </html>
    """

def create_tables_from_aggregations(aggregations: List[AggregatedMeasurement]) -> List[str]:
    
    # group aggregations by city
    aggregations_by_city = {}
    for aggregation in aggregations:
        if aggregation.city not in aggregations_by_city:
            aggregations_by_city[aggregation.city] = []
        aggregations_by_city[aggregation.city].append(aggregation)

    # create html table for each city
    #  which shows the latest value for each param as well as the last updated local time
    html_tables = []
    for city in aggregations_by_city:
        html_tables.append(
            f"""
            <h2>{city}</h2>
            <table>
                <tr>
                    <th>param</th>
                    <th>unit</th>
                    <th>aggregated value</th>
                    <th> number of measurements</th>
                    <th>last updated local time</th>
                </tr>
                {"".join([create_html_row(aggregation) for aggregation in aggregations_by_city[city]])}
            </table>
            """
        )
    return html_tables

def create_html_row(aggregation: AggregatedMeasurement) -> str:
    return f"""
        <tr>
            <td>{aggregation.param}</td>
            <td>{aggregation.unit}</td>
            <td>{'{:.2f}'.format(aggregation.aggregated_value)}</td>
            <td>{aggregation.number_of_measurements_in_window}</td>
            <td>{aggregation.lastest_measurement_time_local}</td>
        </tr>
    """

