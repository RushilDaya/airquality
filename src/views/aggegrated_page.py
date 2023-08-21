from typing import List
from src.models.aggregratedmeasurement import AggregatedMeasurement


def create_aggregated_page(aggregations: List[AggregatedMeasurement]) -> str:
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
                    th {{
                        background-color: #4CAF50;
                    }}
                </style>
            </head>
            <body>
            <h1>Current Air Quality Indicators for Belgian Cities</h1>
                {"".join(aggregation_tables(aggregations))}
            </body>
        </html>
    """

def aggregation_tables(aggregations: List[AggregatedMeasurement]) -> List[str]:
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
                    <th>number of measurements</th>
                    <th>last updated local time</th>
                </tr>
                {"".join([aggregation_row(aggregation) for aggregation in aggregations_by_city[city]])}
            </table>
            """
        )
    return html_tables


def aggregation_row(aggregation: AggregatedMeasurement) -> str:
    return f"""
        <tr>
            <td>{aggregation.param}</td>
            <td>{aggregation.unit}</td>
            <td>{'{:.2f}'.format(aggregation.aggregated_value)}</td>
            <td>{aggregation.number_of_measurements_in_window}</td>
            <td>{aggregation.lastest_measurement_time_local}</td>
        </tr>
    """
