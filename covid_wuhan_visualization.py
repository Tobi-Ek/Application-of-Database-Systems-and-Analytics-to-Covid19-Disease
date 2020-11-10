#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.graph_objects as go

import pycountry
import plotly.express as px
from collections import namedtuple


# In[ ]:





# In[3]:


dap= pd.read_csv('covid_wuhan.csv')
dap


# In[4]:


dap.head()


# In[5]:


dap.groupby("countriesandterritories")[['cases', 'total_wuhan_visited', 'total_recovered','active_cases']].sum().reset_index()


# In[6]:


dap.groupby('cases').sum()


# In[7]:


total_wuhan_visited = dap.groupby('countriesandterritories').sum()['total_wuhan_visited'].reset_index()
active_cases = dap.groupby('countriesandterritories').sum()['active_cases'].reset_index()
total_recovered = dap.groupby('countriesandterritories').sum()['total_recovered'].reset_index()


# In[8]:


fig = go.Figure()
fig.add_trace(go.Bar(x=total_wuhan_visited['countriesandterritories'],
                y=total_wuhan_visited['total_wuhan_visited'],
                name='total_wuhan_visited',
                marker_color='blue'
                ))
fig.add_trace(go.Bar(x=active_cases['countriesandterritories'],
                y=active_cases['active_cases'],
                name='active_cases',
                marker_color='Red'
                ))
fig.add_trace(go.Bar(x=total_recovered['countriesandterritories'],
                y=total_recovered['total_recovered'],
                name='total_recovered',
                marker_color='Green'
                ))

fig.update_layout(
    title='Worldwide Corona Virus Cases - total_wuhan_visited, active_cases, total_recovered (Bar Chart)',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, 
    bargroupgap=0.1
)
fig.show()


# In[9]:


total_wuhan_visited = dap.groupby(['cases', 'countriesandterritories']).sum()[['total_wuhan_visited']].reset_index()
active_cases = dap.groupby(['cases', 'countriesandterritories']).sum()[['active_cases']].reset_index()
total_recovered = dap.groupby(['cases', 'countriesandterritories']).sum()[['total_recovered']].reset_index()


# In[10]:


total_wuhan_visited = dap.groupby(['cases', 'countriesandterritories']).sum()[['total_wuhan_visited']].reset_index()
active_cases = dap.groupby(['cases', 'countriesandterritories']).sum()[['active_cases']].reset_index()
total_recovered = dap.groupby(['cases', 'countriesandterritories']).sum()[['total_recovered']].reset_index()


# In[11]:


all_countries = total_wuhan_visited['countriesandterritories'].unique()
print("Number of countries/regions with cases: " + str(len(all_countries)))
print("Countries/Regions with cases: ")
for i in all_countries:
    print("    " + str(i))


# In[12]:


print(list(countriesandterritories.name for countriesandterritories in pycountry.countries))


# In[13]:


total_wuhan_visited = total_wuhan_visited.copy()
active_cases = active_cases.copy()
total_recovered = total_recovered.copy()
bubble_plot_daps = [total_wuhan_visited, active_cases, total_recovered]


# In[14]:


countries = {}
for countriesandterritories in pycountry.countries:
    countries[countriesandterritories.name] = countriesandterritories.alpha_3
    
total_wuhan_visited["iso_alpha"] = total_wuhan_visited["countriesandterritories"].map(countries.get)
active_cases["iso_alpha"] = active_cases["countriesandterritories"].map(countries.get)
total_recovered["iso_alpha"] = total_recovered["countriesandterritories"].map(countries.get)


# In[15]:


plot_data_total_wuhan_visited = total_wuhan_visited[["iso_alpha","total_wuhan_visited", "countriesandterritories"]]
plot_data_active_cases = active_cases[["iso_alpha","active_cases"]]
plot_data_recovered = total_recovered[["iso_alpha","total_recovered"]]


# In[16]:


fig = px.scatter_geo(plot_data_total_wuhan_visited, locations="iso_alpha", color="countriesandterritories",
                     hover_name="iso_alpha", size="total_wuhan_visited",
                     projection="natural earth", title = 'Total_Wuhan_Visited')
fig.show()


# In[17]:


fig = px.scatter_geo(plot_data_active_cases, locations="iso_alpha", color="active_cases",
                     hover_name="iso_alpha", size="active_cases",
                     projection="natural earth", title="Worldwide Active Cases")
fig.show()


# In[18]:


fig = px.scatter_geo(plot_data_recovered, locations="iso_alpha", color="total_recovered",
                     hover_name="iso_alpha", size="total_recovered",
                     projection="natural earth", title="Worldwide Recovered Cases")
fig.show()


# In[ ]:




