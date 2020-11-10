#!/usr/bin/env python
# coding: utf-8
We have used sql relational query here.
Step 1)We have loaded all four files which are from the different sources like CSV,XML,WEB SCRAPPING.
Step 2)We have done some preprocessing on each data .We have found relevant column in each dataset.
Step 3)We have create three tables respectively for each dataset based on relevant columns.
Step 4)We have stored all the data of relevant column in each tables respectively.
Step 4)We have used INNER JOIN to fetch important features from each table w.r.t primary key COUNTRY and foreign key country.
Step 5)Store the final result of all files in new csv files.
Step 6)Load the twitter from table and store it a new CSV file for visulization purpose seperately.
# In[4]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sns
import DbConnection as dbcon
get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


import os
os.listdir('data')


# In[6]:


data_csv=pd.read_csv('data/COVID19_open_line_list_file_cleaned.csv')
data_csv.head()


# ## Pre proecessing the data

# In[7]:


data_xml=pd.read_csv('data/covid19_xmlToCSV.csv')
data_xml.head()


# In[8]:


data_xml.info()


# In[9]:


data_xml.dropna(inplace=True)


# In[10]:


data_xml.info()


# In[13]:


## Take important column
data_xml_2=data_xml.loc[:,['countriesAndTerritories','cases','deaths']]
data_xml_2.head()


# In[14]:


data_xml_2.info()


# In[89]:


## Group wise country and cases and death


# In[15]:


data_xml_3=data_xml_2.groupby(['countriesAndTerritories'],as_index=False)['cases','deaths'].agg('sum')


# In[16]:


data_xml_3.head()


# In[17]:


data_xml_3.info()


# ## Create a table in postgre for storing xml file

# In[18]:


table_name='covid19_xml_tbl'


# In[19]:


column_name=['countriesandterritories VARCHAR(100) PRIMARY KEY','cases numeric','deaths numeric']


# In[ ]:


dbcon.create_table(table_name,column_name,dbcon.
                   get_dbCon())


# ## Insert data from data_xml_3 dataframe to covid19_xml_tbl

# In[ ]:


db_column=['countriesandterritories','cases','deaths']
dbcon.insert_csv_table(data_xml_3,table_name,db_column)


# In[20]:


## CHECK the insetion part
dbcon.select_count(table_name,dbcon.get_dbCon())


# ## Pre-Process the web scrapping and store into postgre

# In[21]:


data_web=pd.read_csv('data/web_data_covid19.csv')
data_web.head()


# In[22]:


data_web.info()


# In[23]:


# drop the null variable because I want to analyze data
#data_web.dropna(inplace=True,subset=['ActiveCases'])
data_web.dropna(inplace=True)


# In[24]:


data_web.info()


# In[25]:


data_web.head()


# ### Preprocessing web data 

# In[26]:


data_web.info()


# In[104]:


## Remove comma
## replace empty with 0


# In[27]:


data_web['TotalCases']=data_web['TotalCases'].str.replace(",","")
data_web['TotalCases']=data_web['TotalCases'].str.replace(" ",'0')


# In[28]:


data_web['TotalRecovered']=data_web['TotalRecovered'].str.replace(",","")
data_web['TotalRecovered']=data_web['TotalRecovered'].str.replace(" ","0")


# In[29]:


data_web['TotalDeaths']=data_web['TotalDeaths'].str.replace(",","")
data_web['TotalDeaths']=data_web['TotalDeaths'].str.replace(" ","0")


# In[30]:


data_web['ActiveCases']=data_web['ActiveCases'].str.replace(",","")
data_web['ActiveCases']=data_web['ActiveCases'].str.replace(" ","0")


# In[31]:


data_web['Serious_Critical']=data_web['Serious_Critical'].str.replace(",","")
data_web['Serious_Critical']=data_web['Serious_Critical'].str.replace(" ","0")


# In[32]:


data_web.head()


# In[33]:


data_web.info()


# In[34]:


data_web['TotalCases']=data_web['TotalCases'].astype('float64')


# In[35]:


data_web['TotalDeaths']=data_web['TotalDeaths'].astype('float64')


# In[36]:


data_web['TotalRecovered']=data_web['TotalRecovered'].astype('float64')


# In[37]:


data_web['ActiveCases']=data_web['ActiveCases'].astype('float64')


# In[38]:


data_web['Serious_Critical']=data_web['Serious_Critical'].astype('float64')


# In[39]:


table_name='covid19_web_tbl'


# In[40]:


column_name=['country VARCHAR(100)','total_case numeric','total_death VARCHAR(100)','total_recovered string',
             'active_cases numeric','serious_critical numeric']


# In[ ]:


dbcon.create_table(table_name,column_name,dbcon.get_dbCon())


# ### Insertion of web data(data_web) into postgres (covid19_web_tbl)

# In[41]:


db_col=['country','total_case','total_death','total_recovered',
             'active_cases','serious_critical']


# In[ ]:


dbcon.insert_csv_table(data_web,table_name,db_col)


# In[42]:


## Check the insertion
dbcon.select_count(table_name,dbcon.get_dbCon())


# # Relational query INNER JOIN on three tables -covid19_xml_tbl,covid19_web_tbl,country_wuhan_visit_tbl
Show relation query 
Three table we are going to fetch-There data sources are csv ,xml,web scrapping
Table name ,primary key,column names,column name we need to fetch
1)country_wuhan_visit_tbl(country) -['country','total_wuhan_visited']

2)covid19_xml_tbl(countriesandterritories)-['countriesandterritories','cases','deaths']
3)covid19_web_tbl(country)-['country','total_case','total_death','total_recovered',
             'active_cases','serious_critical']
             
We will use inner join here




# In[43]:


query="""
SELECT covid19_xml_tbl.countriesandterritories,
covid19_xml_tbl.cases,
country_wuhan_visit_tbl.total_wuhan_visited,
covid19_web_tbl.total_recovered,
covid19_web_tbl.active_cases
FROM covid19_xml_tbl
 INNER JOIN covid19_web_tbl ON covid19_xml_tbl.countriesandterritories = covid19_web_tbl.country
 INNER JOIN country_wuhan_visit_tbl ON country_wuhan_visit_tbl.country= covid19_web_tbl.country"""




# In[44]:


all_data_df=dbcon.select_res_dataframe(query)


# In[45]:


all_data_df.head()


# In[46]:


all_data_df.info()


# ## Insert fetched data from db to    csv file

# In[47]:


filename=os.getcwd()+"all_file_covid_data.csv"


# In[48]:


filename


# In[49]:


df_all_n=dbcon.insert_df_into_csv(all_data_df,filename)


# In[50]:


df_all_n.head()


# ## TWITTER data manipulation

# ##  Save twitter json  data from postgres table to csv file

# In[51]:


table_name='tweet_json_tbl'
query="SELECT * FROM "+ table_name


# In[52]:


df_json_twitter=dbcon.select_res_dataframe(query)


# In[53]:


df_json_twitter.head()


# In[54]:


df_json_twitter.info()


# In[55]:


df_json_twitter.dropna(subset=['location'],inplace=True)


# In[56]:


df_json_twitter.info()


# In[57]:


file_name='/tweet_json.csv'
filpath=os.getcwd()+file_name


# In[58]:


df_tweet_new=dbcon.insert_df_into_csv(df_json_twitter,filpath)


# In[59]:


df_tweet_new.head()


# In[60]:


df_tweet_new.info()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




