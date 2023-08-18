# Store of all configuration variables
# mix of environment variables and hard-coded values

import os

# default values are for the production environment
# can be overided by environment variables for local development if needed
# this approach can be improved to be more protective over the production environment
# consider using something like secrets manager for the production values

AWS_PROFILE = os.environ.get('AWS_PROFILE', None)
AWS_REGION = os.environ.get('AWS_REGION', 'eu-west-1')

MEASUREMENTS_TABLE = os.environ.get('MEASUREMENTS_TABLE', 'airmax-rushildaya-aq-measurements')
AGGREGATIONS_TABLE = os.environ.get('AGGREGATIONS_TABLE', 'airmax-rushildaya-aq-aggregations')
S3_VIEW_BUCKET = os.environ.get('S3_VIEW_BUCKET', 'rushildaya-aq-results')

# behaviour of the aggregation process
AGGREGATION_WINDOW_HOURS = 3