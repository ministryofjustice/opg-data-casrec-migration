This is a helper script for generating response json from CSV inputs to use in our tests.

Even if you are manually inputting the data, I would suggest starting with this to show you
how the tests will expect it to look.

You can put the cases you want to use in the respective csvs in the root of this folder and it will go and pull
the relevant data from whichever API you choose.

When adding a new API, you should be able to tweak the script by adding a new headers list to it and adding the new csv
type to the csv list.

When you have a data set you are happy with then you can copy it into the following folder:

```
migration_steps/validation/api_test_data_s3_upload/app/validation/csvs
```

Copy full responses into the responses folder if you wish to use them.
