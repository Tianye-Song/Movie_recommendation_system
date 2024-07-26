For MongoDB existing data and future data
Data sources:
1. Kafka
users
views_history

2. Public API
movies
rates

Possible issues:
1. Missing data (check daily based on the model training) (tell liangwei to use the data before a 2. specific time to train the model to avoid quality issues)
3. Duplicate data(already fixed by upserting )
4. Data schema issues (missing feature column) 
5. Possible white space for string data
5. Integer range and format(age 0~100)  (rating 1~5) (could be str, float or null value)
6. Datetime string data to datetime type (carefull for date that month is bigger than 12 and day is smaller than 12)


API request
Now if the user id is in the database, we send model recommendation, when the user id is not in the database, we send random recommendation

Possilble issues: 
1. invalid request, the user id is invalid like letters or null



