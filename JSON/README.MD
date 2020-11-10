We have done following operation on each file:-
1)File-covid19_tweet_json_fetch_api_store_in_postgres
We are working on twitter data here.
Step 1)We have loader first developer key to fetch data from twitter
Step 2)We have made request to twitter to give tweets related to covid19.We have passed hashtag which is popular for 
covid 19 ['#covid19', '#lockdown', '#socialdistancing']
Step 3)We have stored the tweets json in text file.
Step 4)We have read the text file and find out important information and stored these value in new dataframe
Step 5)Created a new table tweet_json_tbl and stored the value from data frame.

2)File-covid_19_Csv_clean_process
Cleaning of CSV file
Step 1)We have loaded two csv files.
Step 2)We have done Data wrangling on both the csv files.
Step 3)We have balanced the missing data ,We have removed unwanted features.
Step 4)Stored the new dataframe in a new csv files.

3)File-Covid_19_forecast_ARIMA_and_AUTO_ARIMA
We have plotted the forecast of Death,confirmed,recovered.
Step 1)We have loaded the CSV files.
Step 2)We have created new dataframe with the index on date.
Step 3)We have created a timeseries with frequence day wise
Step 4)We have plotted autocorrelation graphs.
Step 5)We have plotted Arima model by passing apprpriate value of p,d,q.
Step 6)We have plotted Auto Arima model which will automatically select the value of p,d,q which will give the best AIC
Step 7)Step 2 to Step 6 is same for forecasting death,recovered,confirmed cases.

4)File-covid_data_postgres_relation_query_on_tables
We have used sql relational query here.
Step 1)We have loaded all four files which are from the different sources like CSV,XML,WEB SCRAPPING.
Step 2)We have done some preprocessing on each data .We have found relevant column in each dataset.
Step 3)We have create three tables respectively for each dataset based on relevant columns.
Step 4)We have stored all the data of relevant column in each tables respectively.
Step 4)We have used INNER JOIN to fetch important features from each table w.r.t primary key COUNTRY and foreign key country.
Step 5)Store the final result of all files in new csv files.
Step 6)Load the twitter from table and store it a new CSV file for visulization purpose seperately.

5)File-tweet_Covid19_data_analysis
Find out most populat tag in England and India   respectively  so that people can start following it.
Step 1)Load the cleaned CSV  data of twitter.
Step 2)Preprocessing the data
Step 3)Filter out the data of UK and India.
Step 4)Find out top 5 popular tag in each country
Step 5)Show with bar graph most popular 5 tags.

6)File-tweet_Covid19_data_analysis
Find out most populat tag in England and India   respectively  so that people can start following it.
Step 1)Load the cleaned CSV  data of twitter.
Step 2)Preprocessing the data
Step 3)Filter out the data of UK and India.
Step 4)Find out top 5 popular tag in each country
Step 5)Show with bar graph most popular 5 tags.


