import os

# the default values are for the production system
# for local development, you can override these values by setting them in your environment
PROFILE = os.environ.get('AWS_PROFILE', 'default')
REGION = os.environ.get('AWS_REGION', 'eu-west-1')
MEASUREMENTS_TABLE = os.environ.get('MEASUREMENTS_TABLE', 'airmax-rushildaya-aq-measurements')