#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio


# In[2]:


dap=pd.read_csv('covid_xml.csv')
dap


# In[3]:


dap.info()


# In[4]:


dap.describe()


# In[5]:


dap.isnull().sum()


# In[6]:


top = dap[dap['year'] == dap['year'].max()]
world = top.groupby('countriesAndTerritories')['cases','deaths'].sum().reset_index()
world.head()


# In[7]:


figure = px.choropleth(world, locations="countriesAndTerritories", 
                    locationmode='country names', color="cases", 
                    hover_name="countriesAndTerritories", range_color=[1,20000], 
                    color_continuous_scale="Peach", 
                    title='Countries with Cases')
figure.show()


# In[8]:


world['size'] = world['deaths'].pow(0.2)
fig = px.scatter_geo(world, locations="countriesAndTerritories",locationmode='country names', color="deaths",
                     hover_name="countriesAndTerritories", size="size",hover_data = ['countriesAndTerritories','deaths'],
                     projection="natural earth",title='Death count of each country')
fig.show()


# In[19]:


top = dap[dap['month'] == dap['month'].max()]
top_casualities = top.groupby(by = 'countriesAndTerritories')['cases'].sum().sort_values(ascending = False).head(300).reset_index()
top_casualities


# In[35]:


china =  dap[dap.countriesAndTerritories == 'China']
china = china.groupby(by = 'day')['cases', 'deaths'].sum().reset_index()
china.head()


# In[36]:


plt.figure(figsize=(15,30))
a = plt.subplot(4, 1, 1)
sns.pointplot(china.index ,china.cases)
plt.title("China's Confirmed Cases Over Time" , fontsize = 25)
plt.ylabel('Total cases', fontsize = 15)
plt.xlabel('No. of days', fontsize = 15)


# In[39]:


plt.figure(figsize=(15,30))
plt.subplot(4, 1, 1)
sns.pointplot(china.index ,china.deaths, color = 'g')
plt.title("China's Deaths Cases Over Time" , fontsize = 25)
plt.xlabel('No. of Days', fontsize = 15)
plt.ylabel('Total cases', fontsize = 15)


# In[42]:


china =  dap[dap.countriesAndTerritories == 'China']
china = china.groupby(by = 'month')['cases', 'deaths'].sum().reset_index()
china.head()


# In[43]:


plt.figure(figsize=(15,30))
a = plt.subplot(4, 1, 1)
sns.pointplot(china.index ,china.cases)
plt.title("China's Confirmed Cases Over Time" , fontsize = 25)
plt.ylabel('Total cases', fontsize = 15)
plt.xlabel('No. of month', fontsize = 15)


# In[44]:


plt.figure(figsize=(15,30))
a = plt.subplot(4, 1, 1)
sns.pointplot(china.index ,china.cases)
plt.title("China's Death Cases Over Time" , fontsize = 25)
plt.ylabel('Total cases', fontsize = 15)
plt.xlabel('No. of month', fontsize = 15)


# In[ ]:




