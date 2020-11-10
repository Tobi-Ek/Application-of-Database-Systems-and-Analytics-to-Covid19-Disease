#!/usr/bin/env python
# coding: utf-8
Find out most populat tag in England and India   respectively  so that people can start following it.
Step 1)Load the cleaned CSV  data of twitter.
Step 2)Preprocessing the data
Step 3)Filter out the data of UK and India.
Step 4)Find out top 5 popular tag in each country
Step 5)Show with bar graph most popular 5 tags.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


data=pd.read_csv('data/Cleaned_Tweet_data.csv')


# In[3]:


data.head()


# In[4]:


data.describe()


# In[5]:


data.info()


# ## Drop the null values

# In[6]:


data.dropna(inplace=True)


# In[7]:


data.info()


# In[8]:


data.describe(include='O')


# # Show top  hastags for covid 19

# In[9]:


data['Country'].value_counts()


# ### Popular hashtag in UK

# In[10]:


data_India=data[data['Country']=='UK']
top_has_tag=data_India['hashtags'].value_counts().sort_values(ascending=False)[0:5]
data_hastag=pd.DataFrame(data=top_has_tag.values,index=top_has_tag.index,columns=['hashtag'])


# In[11]:


data_hastag.plot(kind='bar')
plt.title('Top 5 popular hashtag in UK')
plt.show()

We can see that most popular hashtags in UK are COVID19,covid19,lockdown,panicbuying,remotework.
These are tags people should start following in hashtag in UK
# In[12]:


## Top 5 popular hashtag In India


# In[13]:


data_India=data[data['Country']=='India']


# In[14]:


top_has_tag=data_India['hashtags'].value_counts().sort_values(ascending=False)[0:5]


# In[15]:


top_has_tag.values


# In[16]:


data_hastag=pd.DataFrame(data=top_has_tag.values,index=top_has_tag.index,columns=['hashtag'])


# In[17]:


data_hastag.head()


# In[18]:


data_hastag.plot(kind='bar')
plt.title('Top 5 popular hashtag in India')
plt.show()

We can see that most popular hashtags in India are COVID19,Lockdown,Covid19,tax,Robots
These are tags people should start following in hashtag in India
# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




