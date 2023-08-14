# airquality

# what to do next:
still quite a lot to do ofc
as there is basically no data coming through on the expected topic i have my
doubts that it will actually work / give us sufficient data.I am gonna assume its
not going to work properly and as such i will define my own data
-> create a dataset which i can use to seed the database via sqs (figure out how to make it properly structured)
-> quick scripts to do the seeding / cleanup as needed 
-> write a function to do the aggregations think about what we can feasibly achieve
given the limitation of the data.
-> understand how best to integrate this aggregation code into the function...when should it ideally run -> what corners can we cut
-> present layer: MVP is to make some graphs which can be served from an s3 bucket if possible
-> lambda / dynamo / s3 setup do be implemented in terraform