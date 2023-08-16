# airquality

# what to do next:
still quite a lot to do ofc
as there is basically no data coming through on the expected topic i have my
doubts that it will actually work / give us sufficient data.I am gonna assume its
not going to work properly and as such i will define my own data
-> write a function to do the aggregations think about what we can feasibly achieve
given the limitation of the data.
-> understand how best to integrate this aggregation code into the function...when should it ideally run -> what corners can we cut
-> present layer: MVP is to make some graphs which can be served from an s3 bucket if possible
-> lambda / dynamo / s3 setup do be implemented in terraform

* issue: the key doesn't account for the same time but different parameters: need to fix that - for now being optimistic in using different timestamps for the values