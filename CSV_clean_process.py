#!/usr/bin/env python
# coding: utf-8
Cleaning of CSV file
Step 1)We have loaded two csv files.
Step 2)We have done Data wrangling on both the csv files.
Step 3)We have balanced the missing data ,We have removed unwanted features.
Step 4)Stored the new dataframe in a new csv files.
# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


import os
os.listdir('data')


# In[3]:


#Load the csv file
dfol=pd.read_csv('data/COVID19_open_line_list.csv')
dfd=pd.read_csv('data/covid_19_data.csv')


# In[4]:


# data information
dfol.head()


# In[5]:


dfol.info()


# In[6]:


dfd.head()


# In[7]:


dfd.info()


# ### Clean the COVID19_open_line_list

# In[8]:


dfol.head()


# In[9]:


dfol.info()


# In[10]:


dfol.describe()

To make it easier, we created this new complete step-by-step guide in Python. You’ll learn techniques on how to find and clean:

    Missing Data
    Irregular Data (Outliers)
    Unnecessary Data — Repetitive Data, Duplicates and more
    Inconsistent Data — Capitalization, Addresses and more


# In[11]:


## data shape and data types
print(dfol.shape)
print(dfol.dtypes)


# In[12]:


## Select numeric columns
dfol_numeric=dfol.select_dtypes(include=[np.number])
numeric_cols=dfol_numeric.columns.values
print(numeric_cols)


# In[13]:


## Select non-numeric columns
dfol_non_numeric=dfol.select_dtypes(exclude=[np.number])
non_numeric_cols=dfol_non_numeric.columns.values
print(non_numeric_cols)


# ## Missing data

# In[14]:


## Technique 1 Heat Map
cols=dfol.columns[:32] ## first 32 columns
colours = ['#000099', '#ffff00'] # specify the colours - yellow is missing. blue is not missing.
sns.heatmap(dfol[cols].isnull(),cmap=sns.color_palette(colours))
plt.show()

The chart below demonstrates the missing data patterns of the first 30 features. The horizontal axis shows the feature name; the vertical axis shows the number of observations/rows; the yellow color represents the missing data while the blue color otherwise.
# ## Technique 2: Missing Data Percentage List

# In[15]:


for col in dfol.columns:
    pct_missinng=np.mean(dfol[col].isnull())
    print('{} {}%'.format(col,round(pct_missinng*100)))


# ## Missing data histogram

# In[16]:


dfol2=dfol.copy()


# In[17]:


# first create missign indicator for features with missing data
for col in dfol2.columns:
    missing=dfol2[col].isnull()
    num_missing=np.sum(missing)
    if num_missing>0:
        print('created a missing indicator {}'.format(col))
        dfol2['{}_is_missing'.format(col)]=missing
        
#then plot the histogram based on the indicator
ismissing_col=[col for col in dfol2.columns if '_is_missing'  in col]
dfol2['num_missing']=dfol2[ismissing_col].sum(axis=1)
dfol2['num_missing'].value_counts().reset_index().sort_values(by='index').plot.bar(x='index',y='num_missing')

Here we can see that
Index 7000 approx has 31 features missing 

# # Solution

# ##  1 Drop the Observation
In statistics, this method is called the listwise deletion technique. In this solution, we drop the entire observation as long as it contains a missing value.

For example, from the missing data histogram, we notice that only a minimal amount of observations have over 35 features missing altogether. We may create a new dataset df_less_missing_rows deleting observations with over 35 missing features.
# In[18]:


# drop the rows with lots of missing values (35 missing values in a row)
ind_missing=dfol2[dfol2['num_missing']>35].index
dfol2 = dfol2.drop(ind_missing, axis=0)


# In[ ]:





# ## Solution #2: Drop the Feature

# In[19]:


# drop the features which has 80  more percent is null
dfol2_less_features=dfol2.copy()
missing_col=[]


# In[20]:


for col in dfol2.columns:
    num_missing=np.mean(dfol2[col].isnull())
    percentage=round(num_missing*100)
    if percentage > 80.0:
        missing_col.append(col)


# In[21]:


missing_col


# In[22]:


dfol2.drop(missing_col,axis=1,inplace=True)


# In[23]:


dfol2.info()


# In[24]:


dfol2_less_features.head()


# In[25]:


# remove is_missing_col
missing_cols=[]


# In[26]:


for col in dfol2.columns:
    if '_is_missing' in col:
        missing_cols.append(col)


# In[27]:


missing_cols


# In[28]:


dfol2.drop(missing_cols,axis=1,inplace=True)


# In[29]:


dfol2.info()


# In[30]:


dfol2.head()


# In[ ]:





# ## Clean the covid_19_data.csv

# In[31]:


dfd.head()


# In[32]:


dfd.info()


# ## Missing data

# In[33]:


## ## Technique 1 Heat Map
cols=dfd.columns[:32] ## first 32 columns
colours = ['#000099', '#ffff00'] # specify the colours - yellow is missing. blue is not missing.
sns.heatmap(dfd[cols].isnull(),cmap=sns.color_palette(colours))
plt.show()

The chart below demonstrates the missing data patterns of the first 30 features. The horizontal axis shows the feature name; the vertical axis shows the number of observations/rows; the yellow color represents the missing data while the blue color otherwise.
# ## Technique 2: Missing Data Percentage List
# 

# In[34]:


for col in dfd.columns:
    pct_missinng=np.mean(dfd[col].isnull())
    print('{} {}%'.format(col,round(pct_missinng*100)))

#Province has  49 % null  values so I removed the Province/State cols
# In[35]:


dfd.drop(columns=['Province/State'],axis=1,inplace=True)


# In[36]:


dfd.info()


# # Store the cleaned data in csv files

# ## Store the COVID19_open_line_list.

# In[37]:


dfol2.head()


# In[38]:


dfol2.info()


# In[39]:


# REMOVE num_missing COLUMN it's of no use now
dfol2.drop(columns=['num_missing'],axis=1,inplace=True)


# In[40]:


dfol2.info()


# In[41]:


## Create a csv file and insert the cleaned data
try:
    filename='save_data/COVID19_open_line_list_file_cleaned.csv';
    dfol2.to_csv(filename,encoding='utf-8',index=False)
except IOError as e:
    print('Error occur during writing of cleaned files:',filename,e)


# ## Store the covid_19_data.¶

# In[42]:


dfd.head()


# In[43]:


dfd.info()


# In[45]:


## Create a csv file and insert the cleaned data
try:
    filename='save_data/covid_19_data_cleaned.csv';
    dfd.to_csv(filename,encoding='utf-8',index=False)
except IOError as e:
    print('Error occur during writing of cleaned files:',filename,e)


# In[ ]:




