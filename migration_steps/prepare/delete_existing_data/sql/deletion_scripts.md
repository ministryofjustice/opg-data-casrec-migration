### Deletion scripts

We have split out the event deletions into a separate file that need to be reintegrated when we run the scripts for real.

Currently it takes too long to run and no amount of indexing or using different joins helps.
It's just a huge amount of data in the events table so we will take the practical approach of just truncating it for our
preproduction runs.
