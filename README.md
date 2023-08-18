# Notes
* lambda timeout set to 15s
* http://rushildaya-aq-results.s3-website-eu-west-1.amazonaws.com/ to see results


# Next Steps:
* put the validation configuration in a accessible .json file
* fix lambda deployment command (currently is a two step process)
* general refactoring ... (ambigious)
* refactor aws commands to be agnostic to the models 
* Infrastructure as code for dynamo,lambda,s3,sqs
* documentation of code (comments / readme / how to run)
* presentation to explain the code / architecture / next steps [1 unit]


# Known Issues:
* Measurement keys do not account for parameter names, the assumption being that we won't get multiple parameters for a composite_location at the same time. This assumption is not robust

* Dynamodb makes an assumption that all parameters will be available at least in the first 1000 items for a partition. This assumption is not robust