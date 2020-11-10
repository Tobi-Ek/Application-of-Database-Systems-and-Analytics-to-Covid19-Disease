#!/usr/bin/env python
# coding: utf-8

# # Web Scrapping by Inspection

# In[1]:


#Webscrapping Part1

#Webscrapping is applied to worldometers to extract Covid-19 data

#import libraries
import requests
import lxml.html as lh
import pandas as pd

#Scrape table Cells
url='https://www.worldometers.info/coronavirus/'

#Create a handle, page, to handle the contents of the website
page = requests.get(url)

#Store the contents of the website under container
container = lh.fromstring(page.content)

#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = container.xpath('//tr')


# In[2]:


#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]


# In[3]:


#Testing
tr_elements[1][1].text


# In[4]:


tr_elements = container.xpath('//tr')

#Create empty list
col=[]
i=0

#For each row, store each first element (header) and an empty list
for x in tr_elements[0]:
    i+=1
    name=x.text_content()
    print (('%d:"%s"')%(i,name))
    col.append((name,[]))
	
#Since the first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #Td is our j'th row
    Td=tr_elements[j]
    
    #If row is not of size 10, the //tr data is not from our table 
    #if len(Td)!=10:
        #break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for x in Td.iterchildren():
        data=x.text_content()
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1

#Testing to check content of col
#print(col)


# In[5]:


#To check length of the column are the same 
[len(C) for (title,C) in col]


# In[6]:


#Create the Dataframe
Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)

# Show sample of the dataframe
df.head()


# # Insert Into MongoDB

# In[18]:


#Import into MongoDB
import pymongo 
from pymongo import MongoClient

mng_client = pymongo.MongoClient('localhost', 27017) # Making a Connection with MongoClient
mng_db = mng_client['WorldometerDatabase'] # Replace mongodb name
collection_name = 'Worldometer' # Replace mongodb collection name
db_cm = mng_db[collection_name]

#Insert Data 
db_cm.insert_one({"index":"World","Web_Data":Dict})


# # Retrieve from MongoDB

# In[24]:


data_from_db = db_cm.find_one({"index":"World"})
dfmongo = pd.DataFrame(data_from_db["Web_Data"])

dfmongo.head() # view sample of the dataframe

# print(dfmongo) # print the dataframe


# # Export Worldometer Dataframe to CSV file

# In[12]:


#Export Dataframe to CSV file
dfmongo.to_csv (r'C:\Users\presi\export_worldometer.csv', index = False, header=True)


# In[ ]:





# # Web Scrapping by API Call

# In[35]:


#Webscrapping Part2

#API Call will be used for this part of webscrapping

#import the needed library
import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. 
# Hence, the reason we specicified 'None' to replace inputs for application token, and no username or password:
client = Socrata("data.medicare.gov", None)


# To extract First 2000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
hospdata = client.get("xubh-q36u", limit=2000)

# Convert to pandas DataFrame
hospital_data = pd.DataFrame.from_records(hospdata)

# Show sample of the dataframe
hospital_data.head()


# In[36]:


data_dict = hospital_data.to_dict("records")


# # Insert into MongoDB

# In[39]:


#Import into MongoDB
import pymongo 
from pymongo import MongoClient

mng_client = pymongo.MongoClient('localhost', 27017) # Making a Connection with MongoClient
mng_db = mng_client['WorldometerDatabase'] # Replace mongodb name
collection_name = 'Hospital' # Replace mongodb collection name
hb_cm = mng_db[collection_name]

#Insert Data 
hb_cm.insert_one({"index":"USA","Hospital_Data":data_dict})


# # Retrieve from MongoDB

# In[40]:


data_from_db2 = hb_cm.find_one({"index":"USA"})
hfmongo = pd.DataFrame(data_from_db2["Hospital_Data"])

hfmongo.head() # view sample of the dataframe

# print(dfmongo) # print the dataframe


# # Export Hospital Dataframe to CSV file

# In[ ]:


#Export Dataframe to CSV file
hfmongo.to_csv (r'C:\Users\presi\export_hospital_data.csv', index = False, header=True)

