#!/usr/bin/env python
# coding: utf-8
We are working on twitter data here.
Step 1)We have loader first developer key to fetch data from twitter
Step 2)We have made request to twitter to give tweets related to covid19.We have passed hashtag which is popular for 
covid 19 ['#covid19', '#lockdown', '#socialdistancing']
Step 3)We have stored the tweets json in text file.
Step 4)We have read the text file and find out important information and stored these value in new dataframe
Step 5)Created a new table tweet_json_tbl and stored the value from data frame.

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
from  psycopg2.extensions import connection as DB_CON
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Fetch twitter developer token 

# In[1]:


# I have not shared the my personal token key.It is not advisable to share your personal key


# In[ ]:


key_file='/Users/rahul/Documents/twitter/private_keys_developer/twitter_keys.txt'
try:
    file= open(key_file,'r')
    key_dic={}
    for f in file.readlines():
        if f!='\n':
            f=f.replace('\n','')
            key_value=f.split(':')
            key_dic[key_value[0]]=key_value[1]
except IOError as e:
    print('File reading error',e)
        


# In[ ]:


access_token = key_dic['Access_token']
access_token_secret = key_dic['Access_token_secret']
consumer_key = key_dic['Api_Key']
consumer_secret = key_dic['Api_secret_key']


# ## Create a text file to store the tweets json

# In[ ]:


try:
    tweets_data_path = "twitter_data_1.txt"  
    tweets_file=open(tweets_data_path,'w')
except IOError as e:
    print(e)


# ## Fetch the tweet from twitter based on hastag -['#covid19', '#lockdown', '#socialdistancing']

# In[ ]:


#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re

# Enter Twitter API Keys
access_token = key_dic['Access_token']
access_token_secret = key_dic['Access_token_secret']
consumer_key = key_dic['Api_Key']
consumer_secret = key_dic['Api_secret_key']

# Create tracklist with the words that will be searched for
tracklist = ['#covid19', '#lockdown', '#socialdistancing']
# Initialize Global variable
tweet_count = 0
# Input number of tweets to be downloaded
n_tweets = 1000



# Create the class that will handle the tweet stream
class StdOutListener(StreamListener):
      
    def on_data(self, data):
        global tweet_count
        global n_tweets
        global stream
        if tweet_count < n_tweets:
            print(data)
            tweets_file.writelines(data)
            tweet_count += 1
            return True
        else:
            stream.disconnect()

    def on_error(self, status):
        print(status)



# Handles Twitter authetification and the connection to Twitter Streaming API
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track=tracklist)
tweets_file.close()


# In[5]:


def find_hash(hash_text:list):
        if len(hash_text)==0:
            return None
        else:
            return hash_text[0]['text']
        


# ## Create a dataframe to store the important values from json

# In[6]:


import json
import pandas as pd
tweets_data_path = "twitter_data_1.txt"  
tweets_data = []  
tweets_file = open(tweets_data_path, "r")  
for line in tweets_file:  
    try:  
        tweet = json.loads(line)  
        tweets_data.append(tweet) 
    except Exception as e:
        print(e)
        
tweets = pd.DataFrame()
tweets['id'] = list(map(lambda tweet: tweet['id'], tweets_data))
tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
tweets['user_name'] = list(map(lambda tweet: tweet['user']['screen_name'], tweets_data))
tweets['created_at'] = list(map(lambda tweet: tweet['created_at'], tweets_data))
tweets['location'] = list(map(lambda tweet: tweet['user']['location'], tweets_data))
tweets['timestamp_ms'] = list(map(lambda tweet: tweet['timestamp_ms'], tweets_data))
tweets['quote_count'] = list(map(lambda tweet: tweet['quote_count'], tweets_data))
tweets['reply_count'] = list(map(lambda tweet: tweet['reply_count'], tweets_data))
tweets['retweet_count'] = list(map(lambda tweet: tweet['retweet_count'], tweets_data))
tweets['favorite_count'] = list(map(lambda tweet: tweet['favorite_count'], tweets_data))
tweets['hashtags'] = list(map(lambda tweet: find_hash(tweet['entities']['hashtags']), tweets_data))
tweets.head()


# In[7]:


tweets.info()


# # DB operation

# ## Get connection fn

# In[68]:


def get_dbCon():
        try:
            conn=psycopg2.connect(host='localhost',port=5432,database="postgres",user='postgres',password="RamP")
            return conn
        except Exception as e:
            print('Db connection occurred-',e)
            
        


# ## rows count fn

# In[69]:


def select_row_count(table_name,conn:DB_CON):
    query="SELECT count(*) FROM "+table_name+" "
    cur=conn.cursor()
    cur.execute(query)
    query_results=cur.fetchall()
    print(query_results)
    conn.close()


# ## Create table fn

# In[70]:


def create_table(table_name:str,column_detail_nameList:list,conn:psycopg2.extensions.connection):
    try:
        cursor=conn.cursor()
        create_table_query= "CREATE TABLE "+table_name+" (";
        cnt=0
        for col_detail in column_detail_nameList:
            if cnt==0:
                create_table_query+= " "+ col_detail
                cnt=1
            else:
                create_table_query+= " ,"+ col_detail
        create_table_query+=" );"
        cursor.execute(create_table_query)
        conn.commit()
        print(table_name,"-Table created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)
    finally:
            #closing database connection.
        if(conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

    


# ## Insert table fn

# In[74]:


from sqlalchemy import create_engine
def insert_df_table(df:pd.DataFrame,table_name:str,db_cols:list):
    try:
        engine = create_engine('postgresql://postgres:RamP@localhost:5432/postgres')
        
        (df.rename(columns=dict(zip(df.columns,db_cols)))
             .to_sql(name=table_name,con=engine,if_exists="append",index=False,index_label=None,schema='public'))
        print('Data insert succecssfull into the ',table_name )
    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while inserting PostgreSQL table", error)
    finally:
            #closing database connection.
            print("PostgreSQL connection is closed")


# In[72]:


tweets.info()


# ## 2)Create table tweet_json_tbl

# In[73]:


#COVID19_open_line_list_file_cleaned
table_name='tweet_json_tbl'
column_name=['id numeric PRIMARY KEY','text TEXT','user_name VARCHAR (100)','created_at VARCHAR (100)',
            'location VARCHAR(100)','timestamp_ms numeric','quote_count numeric','reply_count numeric',
            'retweet_count numeric','favorite_count  numeric','hashtags TEXT']

create_table(table_name,column_name,get_dbCon())


# ## 2.1) Insert tweet json into tweet_json_tbl

# In[76]:


db_cols=['id','text','user_name','created_at',
            'location','timestamp_ms','quote_count','reply_count',
            'retweet_count','favorite_count','hashtags']
table_name='tweet_json_tbl'

insert_df_table(tweets,table_name,db_cols)


# In[77]:


select_row_count(table_name,get_dbCon())


# In[ ]:




