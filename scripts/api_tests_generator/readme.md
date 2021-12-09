This is a helper script for generating response json from CSV inputs to use in our tests.

Even if you are manually inputting the data, I would suggest starting with this to show you
how the tests will expect it to look.

You can put the cases you want to use in the respective csvs in the root of this folder and it will go and pull
the relevant data from whichever API you choose.

Steps to creating API tests:
- Log into a local sirius and find an example case that has the entity you're looking at on
- Use inspect in your browser to look for which API request (will be in network tab under sub tab of headers)
- Grab out the response json and add it to the examples folder. This is so we can refer back to it if we want to add
further tests later!
- Create a cut down csv for your entity as per the other files in the root of this directory.
It should only have 4 header fields and should look something like this (but with cases that have the relevant
entity on them):

```
endpoint,entity_ref,test_purpose,full_check
/api/v1/clients/{id},10000037,dev_api_tests,FALSE
/api/v1/clients/{id},10000088,dev_api_tests,FALSE
```

- Make sure you use the endpoint path that you found from inspecting the frontend!
- Find some relevant fields that you would like to bring back data for and add them under an entity
object in the app.py.

Example:
```
clients_headers = [
    '["clientAccommodation"]["handle"]',
    '["salutation"]',
    '["firstname"]',
    '["surname"]',
]
```

- Change or add the entity you're creating under csv in app.py:

```
csvs = ["clients"]
```

- Finally tell the script what base entity type to bring back for this entity so it knows how to fill in the `id` field
from your endpoint. Just have a look at `get_entity_ids` function and you should be able to work out what you need.
- Run the script `python app.py`
- This should create an input files that can be used in the main API tests
- The main completed file now needs to be copied to `migration_steps/api_test_data_s3_upload/app/validation/csvs`
- Modify the `entities` variable in `migration_steps/validation/response_tests/app.py`. You may have to use
others as examples here and follow through the code a bit to get an idea of what it does.
- Now when the tests are run it will upload the file to s3 and use it as part of the tests.

You can also generate Preprod API tests though there is zero benefit in doing so unless you pick the right cases out
(using SQL), give them meaningful `test_purpose` row and check and sign off the results against the
frontend for each case.

In this way you are assuring that data for each use case is correct (you know this by checking manually), that it
doesn't break the application (you know this as response comes back without error for each data combination) and that
it will be regression tested going forward even if someone in the future
makes a mapping change or code change that affects it (as it should affect the response brought back as
you have signed it off as correct).
