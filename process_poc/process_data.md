# Lets process some data!

[TOC]



## <u>Concept</u>

Take one sirius object (ie, a table or part of a table), grab all the data that makes up that object from casrec and morph it into the sirius format.



## <u>Caveats!</u>

This was just a brain dump, written one step at a time, so the code is neither pretty nor effecient. The purpose was to try and work out what steps we'd have to go through to convert one lump of data into another, using the mapping spreadsheet as the 'instructions'.



## <u>Step 1</u> - get the casrec data

Get all of the casrec columns that have been mapped in the mapping doc into a list, and use this to select the appropriate columns from the casrec database into a dataframe



##### Example - persons (Client):

The initial DataFrame looks like this:

|      | DOB        | Title | Forename | Surname | Create     |     Case |
| ---: | :--------- | :---- | :------- | :------ | :--------- | -------: |
|    0 | 2011-05-29 | Mr.   | Lesley   | Bell    | 1996-05-03 | 10000037 |
|    1 | 2018-06-20 | Dr.   | Kate     | Moore   | 1996-06-14 | 10001668 |
|    2 | 2016-12-16 | Mrs.  | Lindsey  | Dale    | 1996-08-12 | 10002199 |

*Caveat*: For the example tables `persons` and `addresses` I've been using to test this, this is super simple as the data only comes from one casrec table. This will get more complex if we have to build one sirius table from multiple casrec tables, but the query that actually gets the initial data can be customised.





## Step 2 - basic column remap

Some columns are just going to be straight field -> field moves, so we can automate this easily

* Get the list of basic mappings from the mapping doc into a dict with format:

  ```python
  {
    'firstname': {
      'casrec_column_name': 'Forename',
      'casrec_table': 'PAT',
      'requires_transformation': 'unknown',
    },
  }
  ```

  *(`unknown` has been added by me, because it's hard to do dataframe queries to find when things are null)*

* Turn these into list of `sirius name`:`casrec name` key-value pairs eg:

  ```Python
  {
    'Case': 'caserecnumber',
    'Create': 'createddate',
    'DOB': 'dob',
    'Forename': 'firstname',
    'Surname': 'surname',
    'Title': 'salutation',
  }
  
  ```

  

* Use these to rename the columns in the original dataframe



##### Example - persons (Client):

DataFrame now looks like this:

|      | dob        | salutation | firstname | surname | createddate | caserecnumber |
| ---: | :--------- | :--------- | :-------- | :------ | :---------- | ------------: |
|    0 | 2011-05-29 | Mr.        | Lesley    | Bell    | 1996-05-03  |      10000037 |
|    1 | 2018-06-20 | Dr.        | Kate      | Moore   | 1996-06-14  |      10001668 |
|    2 | 2016-12-16 | Mrs.       | Lindsey   | Dale    | 1996-08-12  |      10002199 |





## <u>Step 3</u> - transformations

Some columns will require some transformation. At the moment I have only defined 4 of these that I think might end up being standard accross a lot of tables, but who knows.

* Get the list of transformations from the mapping doc - same as the simple mappings above but only looks at rows that have `requires_transformation` not null

* Do some convoluted data wrangling to get these into a nice list (this example is from `addresses (Client)`:

  ```python
  {
    'unique_number': [
      {
        'aggregate_col': 'uid',
        'original_columns': ['unknown'],
      },
    ],
  }
  ```

  *Caveat:* this is very badly named, it's because I started with the address lines which need to be concatenated together :D

  

* Iterate through the list applying the transformations as required (<- this is not very efficient but works for now)

##### Example - persons (Client):

DataFrame now looks like this (I am aware that the `uid` is not actually just a random 12 digit number, but it will do for now!:

|      | dob        | salutation | firstname | surname | createddate | caserecnumber |          uid |
| ---: | :--------- | :--------- | :-------- | :------ | :---------- | ------------: | -----------: |
|    0 | 2011-05-29 | Mr.        | Lesley    | Bell    | 1996-05-03  |      10000037 | 168623462364 |
|    1 | 2018-06-20 | Dr.        | Kate      | Moore   | 1996-06-14  |      10001668 | 894893851736 |
|    2 | 2016-12-16 | Mrs.       | Lindsey   | Dale    | 1996-08-12  |      10002199 | 979921766280 |



##### Example - addresses (Client):

Before transformations applied:

|      | Adrs1              | Adrs2          | Adrs3     | town     | county | postcode | Foreign |
| ---: | :----------------- | :------------- | :-------- | :------- | :----- | :------- | :------ |
|    0 | 803 Gough turnpike | Port Sally     | E1 5ST    |          |        | YO99 7DU | 0.0     |
|    1 | Flat 22            | Palmer islands | Jonesland | JE93 8LU |        | KA9B 3JW | 0.0     |
|    2 | 35 Sylvia vista    | East Ellie     | S6T 4LY   |          |        | KY80 6UH |         |



And after: `foreign` is converted to a bool and renamed to `isairmailrequired` and the address lines are all concatenated and converted to a json array:

|      | town     | county | postcode | address_lines                                  | isairmailrequired |
| ---: | :------- | :----- | :------- | :--------------------------------------------- | :---------------- |
|    0 |          |        | YO99 7DU | ["803 Gough turnpike", "Port Sally", "E1 5ST"] | False             |
|    1 | JE93 8LU |        | KA9B 3JW | ["Flat 22", "Palmer islands", "Jonesland"]     | False             |
|    2 |          |        | KY80 6UH | ["35 Sylvia vista", "East Ellie", "S6T 4LY"]   | False             |





## <u>Step 4</u> - required columns

Some columns are not nullable but yet don't have a database level default, so you can't insert into the Sirius table without setting them to something

* Get the list of required columns from the mapping doc - same as the simple mappings above but only looks at rows that have no mapping, no transformation, do not autoincrement, are not the primary key, must not be null but do not have a default set!

  ```python
  {
    'correspondencebyemail': {
      'data_type': 'bool',
      'default_value': False,
    },
  }
  ```

  

* This `required_columns` dict also contains a `default_value` which I've just filled with nonsense for now, we'll probably have some work to do to figure our what Sirius does with these

##### Example - persons (Client):

DataFrame now looks like this:

|      | dob        | salutation | firstname | surname | createddate | caserecnumber |          uid | correspondencebypost | correspondencebyphone | correspondencebyemail | type           |
| ---: | :--------- | :--------- | :-------- | :------ | :---------- | ------------: | -----------: | :------------------- | :-------------------- | :-------------------- | :------------- |
|    0 | 2011-05-29 | Mr.        | Lesley    | Bell    | 1996-05-03  |      10000037 | 158120497591 | False                | False                 | False                 | default_string |
|    1 | 2018-06-20 | Dr.        | Kate      | Moore   | 1996-06-14  |      10001668 | 940772769536 | False                | False                 | False                 | default_string |
|    2 | 2016-12-16 | Mrs.       | Lindsey   | Dale    | 1996-08-12  |      10002199 | 877280144246 | False                | False                 | False                 | default_string |





## <u>Step 5</u> - Compare with the Sirius table structure

This was a very basic attempt at verifying what we've created, but because we're ignoring a bunch of columns (because they have defaults or we're just leaving them as null) we are only building a subset of this, so it doesn't work. Hence it will always sat `False` and I just ignore it :D



## <u>Step 6</u> - insert into Sirius database

Currently I'm inserting directly into the proper tables in the SIrius dev backup we have locally. Obviously this is not a long term situation, but I needed a way to check that I could actually use the data I'd created!

Because I am inserting into a table that already has data in it, I'm having to do some fiddling around with the `id` as it is a pk so must be unique and not null, so I am getting the `max(id)` from the sirius table and adding that to an incremeting column in the new dataframe so it will insert nicely

##### Example - persons (Client):

DataFrame is now in its final form before inserting!

|      |   id | dob        | salutation | firstname | surname | createddate | caserecnumber |          uid | correspondencebypost | correspondencebyphone | correspondencebyemail | type           |
| ---: | ---: | :--------- | :--------- | :-------- | :------ | :---------- | ------------: | -----------: | :------------------- | :-------------------- | :-------------------- | :------------- |
|    0 |  279 | 2011-05-29 | Mr.        | Lesley    | Bell    | 1996-05-03  |      10000037 | 470950862024 | False                | False                 | False                 | default_string |
|    1 |  280 | 2018-06-20 | Dr.        | Kate      | Moore   | 1996-06-14  |      10001668 | 937478583244 | False                | False                 | False                 | default_string |
|    2 |  281 | 2016-12-16 | Mrs.       | Lindsey   | Dale    | 1996-08-12  |      10002199 | 148153999016 | False                | False                 | False                 | default_string |





## <u>Step 7</u> - join up foreign keys

Not done this yet, as the two tables I've been using to test this are `persons` and `addresses` and these are special because in casrec all this info is held in the `pat` table, so building the keys will work differently to other tables where we have to really join 2 seperate tables together.

TBH this may well have to be custom per table anyway, we'll have to see.



## <u>Next Steps</u>

* Figure out how to make it work with some other tables, find some that are made up of multiple casrec tables if possible
* Figure out how to build some fk relationships between tables
* Formalise the new mapping doc format (don't worry it's not wildly different!)
* If we can recreate all the data in the basic data set with this, then look into how to make the code nicer, faster, testable :D
* Decide where we are inserting the data at the end. Local sirius dev is fine for now

