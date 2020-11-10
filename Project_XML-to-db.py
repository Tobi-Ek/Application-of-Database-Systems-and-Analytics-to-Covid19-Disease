#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xmltodict


# In[2]:


import json


# In[4]:


import xmltodict
import json

with open("COVID_DAP.xml",'r', encoding='utf8') as covid:
    xmlstring=covid.read()
    
jsonString = json.dumps(xmltodict.parse(xmlstring), indent=4)

print(jsonString)


# In[5]:


json_dict = json.loads(jsonString)


# In[6]:


records = json_dict['records']
record = records['record']


# In[7]:


record


# In[8]:


import pymongo
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client.covid
covid_19 = db.covid_19 




# In[9]:


covid_19_data = covid_19.insert_many(record)


# In[10]:


client.list_database_names()


# In[11]:


covid_19_data.inserted_ids


# In[12]:


import pprint
for covid_data in covid_19.find():
    pprint.pprint(covid_data)


# In[13]:


covid_19.count({})


# In[14]:


import pandas as pd
new_covid_data = pd.DataFrame(list(db.covid_19.find()))


# In[15]:


new_covid_data


# ##  Data Preprocessing 

# ### Importing the libraries

# In[16]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# ### Checking Shape , index and columns of the data.

# In[17]:


new_covid_data.shape


# In[18]:


new_covid_data.index


# In[19]:


new_covid_data.columns


# ### Checking for the Missing Values

# In[20]:


new_covid_data.isnull().sum()


# ### Removing the rows having null values

# In[21]:


covid_clean = new_covid_data.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)


# In[22]:


covid_clean.isnull().sum()


# ### Compairing Two data Frames

# In[23]:


print("Old data frame length:", len(new_covid_data), "\nNew data frame length:",  
       len(covid_clean), "\nNumber of rows with at least 1 NA value: ", 
       (len(new_covid_data)-len(covid_clean))) 


# ### Checking Data Types

# In[24]:


covid_clean.dtypes


# ### Deleting non-relevant columns

# In[25]:


covid_clean = covid_clean.drop(['_id','dateRep'],axis=1)


# In[26]:


covid_clean


# ### Checking data Information

# In[27]:


covid_clean.info()


# ### Creating Table in the covid database in postgreql

# ### Converting the covid_clean data into csv file format

# ### Loading covid_clean.csv file into postgresql covid database

# ## Connecting and Loading covid Data into PostgreSQL database i.e. creating covid database

# ### Importing libraries

# In[28]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
from  psycopg2.extensions import connection as DB_CON
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Connecting with PostgreSQL

# In[29]:


def get_dbCon():
        try:
            conn=psycopg2.connect(host='localhost',port=5432,database="postgres",user='postgres',password="RamP")
            return conn
        except Exception as e:
            print('Db connection occurred-',e)


# #### 

# In[30]:


def select_res(table_name,conn:DB_CON):
    query="SELECT count(*) FROM "+table_name+" "
    cur=conn.cursor()
    cur.execute(query)
    query_results=cur.fetchall()
    print(query_results)
    conn.close()


# ### Making Table in PostgreSQL

# In[31]:


table_name ='covid'
col_name = list(covid_clean.head(0))


# ### Inserting covid_clean data into PostgreSQL table

# In[38]:


from sqlalchemy import create_engine
def insert_csv_table(df:pd.DataFrame,table_name:str,db_cols:list):
    try:
        engine = create_engine('postgresql://Ramp:postgres@localhost:5432/Postgres')
       
        (df.rename(columns=dict(zip(df.columns,db_cols)))
             .to_sql(name=table_name,con=engine,if_exists="append",index=False,index_label=None,schema='public'))
        print('Data insert succecssfull into the ',table_name )
    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while inserting PostgreSQL table", error)
    finally:
            #closing database connection.
            print("PostgreSQL connection is closed")


# In[ ]:


insert_csv_table(covid_clean,table_name,col_name)


# 

# In[57]:


select_res(table_name,get_dbCon())


# ### Checking data in covid_clean.

# In[49]:


covid_clean.head()


# ### Fetching  data (covid_clean) from PostgreSQL
# 

# In[66]:


import pandas as pd
import pandas.io.sql as sqlio
import psycopg2

sql = "SELECT * FROM public.covid"
try:
    dbConnection = psycopg2.connect(
        user = "dap",
        password = "dap",
        host = "localhost",
        port = "5432",
        database = "postgres")
    covid_clean_df = sqlio.read_sql_query(sql, dbConnection)
except (Exception , psycopg2.Error) as dbError :
    print ("Error:", dbError)
finally:
    if(dbConnection): dbConnection.close()


# ### Reading data from postgreSQL i.e in table format 

# In[67]:


covid_clean_df


# In[ ]:




