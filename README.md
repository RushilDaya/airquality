# airquality

# what to do next:
still quite a lot to do ofc
as there is basically no data coming through on the expected topic i have my
doubts that it will actually work / give us sufficient data.I am gonna assume its
not going to work properly and as such i will define my own data
-> present layer: MVP is to make some graphs which can be served from an s3 bucket if possible
-> lambda / dynamo / s3 setup do be implemented in terraform
-> centralize environment  variables

* issue: the key doesn't account for the same time but different params: need to fix that - for now being optimistic in using different timestamps for the values

* note i needed to change the lambda timeout away from 3 seconds to 15s

remaining steps now:
make a simple page showing the aggregations (keep it very simple just an html table) which gets updated in s3? 

once this is done i want to take some time for refactoring (few hours)
then i want begin doing IaC (this might be only next monday)