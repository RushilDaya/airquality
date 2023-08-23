# Description
An aws application designed to ingest air  quality data from   https://registry.opendata.aws/openaq/ made available via an SQS queue. The applications  makes available the current (3 hour average) air quality data for Belgian cities for various metrics and hosts the results on publically available webpage

### technical solution
The Solution is implemented in AWS following a serverless architecture. System input comes in the form of openAQ measurements arriving on an SQS queue.
A lambda function listening to this queue performs 3 sequential tasks (can be split out in future)
- Incoming measurements are saved to a measurements table in dynamodb
- for locations/parameter combinations which recieved new measurements, the current airquality (3 hour aggregation) is recomputed and stored in an aggregations table in dynamodb.
- a static web page (hosted in an S3 bucket) is updated with the most recent aggregation data

### folder structure
- dynamo_helpers/
    - non-production grade scripts for validation contents of the dynamodb tables during development.
- exploration/
    - non-production grade code for gaining an initial understanding of the data
- mock_data/
    - scripts for uploading dummy data to an SQS queue, allowing for system testing inspite of unreliable data source.
- src/
    - production code bundled into lambda deployment
- lambda_function.py
    - entry point for AWS lambda function
- lambda_deploy.sh
    - deploy script to take local lambda function code to production
# How to run code
NOTE: How to setup the required infrastructure is not included in this guide
as automated infrastructure creation is not yet implemented
## prerequistes
- an aws lambda function with a trigger on an sqs queue containing openaq measurements (min timeout of 15s)
- a dynamodb table for measurements with partition key composite_location and sort key timestamp_utc
- a dynamodb table for aggregations with partition key composite_location and sort key param
- a publically available s3 bucket with static site hosting enabled

## steps
- update src/config.py to contain the correct urls for your created aws resources
- for a local run first install dependencies with 
    - ```pip install -e . ```
- to deploy the project update the ```aws update-function-code``` with the correct details of your lambda function
- run ```lambda_deploy.sh``` to deploy your code
- ```python mock_data/mock_data_stream.py``` can be run to send realistic mock data to an SQS 

# TODO:
* Infrastructure as code for dynamo,lambda,s3,sqs
* better visualization of measurements data (geospatial)
* fix known issues
* separate out lambda function into multiple functions if needed


# Known Issues:
* Measurement keys do not account for parameter names, the assumption being that we won't get multiple parameters for a composite_location at the same time. This assumption is not robust

* Dynamodb makes an assumption that all parameters will be available at least in the first 1000 items for a partition. This assumption is not robust