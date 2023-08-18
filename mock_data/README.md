The data source intended to be used https://registry.opendata.aws/openaq/ 
Does not appear to be generating sufficent data events
As such for demonstration purposes the seed_sqs.py script can be run
to publish the events stored in mock_data.json to the desired SQS as defined in the seed script.

Has no dependencies with the the production code in (src/)
