#!/usr/bin/env python
# coding: utf-8
We have plotted the forecast of Death,confirmed,recovered.
Step 1)We have loaded the CSV files.
Step 2)We have created new dataframe with the index on date.
Step 3)We have created a timeseries with frequence day wise
Step 4)We have plotted autocorrelation graphs.
Step 5)We have plotted Arima model by passing apprpriate value of p,d,q.
Step 6)We have plotted Auto Arima model which will automatically select the value of p,d,q which will give the best AIC
Step 7)Step 2 to Step 6 is same for forecasting death,recovered,confirmed cases.
# ## Preprocessing  data

# In[1]:


import pandas as pd


# In[2]:


import pandas as pd 


# Import data 

# In[3]:


import io
df = pd.read_csv('data/covid19_date_stats_n.csv')


# In[4]:


df.head()


# In[5]:


df_o=df.copy()


# In[ ]:





# In[ ]:





# In[6]:


df.head()


# In[7]:


df.columns


# ## Death Prediction

# 
# Let's start by dropping tracks with missing features:
# 
# 

# In[8]:


s = df["Deaths"].isna()
indices = s[s == True].index.values.tolist()
df = df.drop(index=indices)
df = df.reset_index()


# Extracting numerical features and the date of every top 200 list:

# In[9]:


features = df.select_dtypes(include=["float64"])


# In[10]:


features.info()


# In[11]:


dates = []
for i in range(0, df.shape[0], 3):
    dates.append(df["ObservationDate"][i][:10])


# In[12]:


dates


# Averaging over every top 200 list and backwards filling missing weeks:

# In[13]:


feature_mean = pd.DataFrame(columns=features.columns, index=pd.to_datetime(dates))
for feature in features.columns:
    average = []
    for i in range(0, df.shape[0], 3):
        average.append(df[feature][i:i+3].mean())
    feature_mean[feature] = average


# In[14]:


feature_mean = feature_mean.asfreq(freq="D", method='bfill')


# In[15]:


feature_mean.info()


# ## Manual forecasting using Autoregressive Integrated Moving Average (ARIMA)

# In[16]:


from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# ARIMA depend on the values p, d, q
# 
# p = number of lags, AR terms
# 
# d = order of differencing
# 
# q = number of lagged forecast errors, MA terms

# In[17]:


timeseries = feature_mean["Deaths"]


# Augmented Dickey Fuller (ADF) test to see if the timeseries is stationary:

# In[18]:


print("p-value:", adfuller(timeseries.dropna())[1])


# The p-value is greater than the significance level 0.05 so it is not stationary and differencing is needed, d > 0

# #### Finding a value for d using autocorrelation:

# In[19]:


fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(311)
fig = plot_acf(timeseries, ax=ax1, title="Autocorrelation on Original Series") 
ax2 = fig.add_subplot(312)
fig = plot_acf(timeseries.diff().dropna(), ax=ax2, title="1st Order Differencing")
ax3 = fig.add_subplot(313)
fig = plot_acf(timeseries.diff().diff().dropna(), ax=ax3, title="2nd Order Differencing")


# The timeseries is stationary at **d = 1** (all but one should be under the significance level) 
# 
# If your series is slightly under differenced, try adding an additional AR and if it is slightly over-differenced, maybe add an additional MA term.

# #### Value for p is the amount of lags bigger than the significance level in partial autocorrelation

# In[20]:


plot_pacf(timeseries.diff().dropna(), lags=40) #knowing d=1 we apply diff() once
plt.show()


# Lag 1 is above the signicance level and so **p = 1**.

# #### Number of q using autocorrelation on the stationary series:

# In[21]:


plot_acf(timeseries.diff().dropna())
plt.show()


# One above the significance level and thus **q = 1**.

# #### Building the model

# In[22]:


model = ARIMA(timeseries, order=(1, 1, 0))
results = model.fit()
results.summary()


# Akaike information criterion (AIC) estimates the relative amount of information lost by a given model. The less the better!

# Now for the prediction:

# In[23]:


graph = results.plot_predict(1, 210)
plt.title('Forecast of death -Arima model')
plt.ylabel('count')
plt.xlabel('Month')
plt.show()


# ## Timeseries forecasting using auto_arima

# In[ ]:





# In[24]:


import pmdarima as pm


# In[25]:


def arimamodel(timeseries):
    automodel = pm.auto_arima(timeseries, 
                              start_p=1, 
                              start_q=1,
                              test="adf",
                              seasonal=False,
                              trace=True)
    return automodel


# In[26]:


def plotarima(n_periods, timeseries, automodel,case_type):
    # Forecast
    fc, confint = automodel.predict(n_periods=n_periods, return_conf_int=True)
    # Weekly index
    fc_ind = pd.date_range(timeseries.index[timeseries.shape[0]-1], periods=n_periods, freq="D")
    # Forecast series
    fc_series = pd.Series(fc, index=fc_ind)
    # Upper and lower confidence bounds
    lower_series = pd.Series(confint[:, 0], index=fc_ind)
    upper_series = pd.Series(confint[:, 1], index=fc_ind)
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.title("Auto Arima model of "+case_type +" Forecast")
    plt.plot(timeseries)
    plt.plot(fc_series, color="red")
    plt.xlabel("date")
    plt.ylabel(timeseries.name)
    plt.fill_between(lower_series.index, 
                     lower_series, 
                     upper_series, 
                     color="k", alpha=.25)
    plt.legend(("past", "forecast", "95% confidence interval"), loc="upper left")
    plt.show()


# In[27]:


automodel = arimamodel(feature_mean["Deaths"])
automodel.summary()


# In[28]:


plotarima(70, feature_mean["Deaths"], automodel,"Deaths")


# ## Discussion

# Manually we got (p, d , q) = (1, 1, 1) and auto_arima found the lowest AIC value at the same parameters!
# 
# It is much less of a hazzle to use the automatic one, except for it not having a built in plot command, but that is a minor flaw IMO.
# 
# Hope this brief summary of ARIMA proved useful :)

# # Confirmed cases prediction

# In[29]:


df_c=df.copy()


# In[30]:


s = df_c["Confirmed"].isna()
indices = s[s == True].index.values.tolist()
df = df_c.drop(index=indices)
df = df_c.reset_index()


# In[31]:


features = df.select_dtypes(include=["float64"])


# In[32]:


dates = []
for i in range(0, df.shape[0], 3):
    dates.append(df["ObservationDate"][i][:10])


# In[33]:


feature_mean = pd.DataFrame(columns=features.columns, index=pd.to_datetime(dates))
for feature in features.columns:
    average = []
    for i in range(0, df.shape[0], 3):
        average.append(df[feature][i:i+3].mean())
    feature_mean[feature] = average


# In[34]:


feature_mean = feature_mean.asfreq(freq="D", method='bfill')


# In[35]:


from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# In[36]:


timeseries = feature_mean["Confirmed"]


# In[37]:


print("p-value:", adfuller(timeseries.dropna())[1])


# In[38]:


fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(311)
fig = plot_acf(timeseries, ax=ax1, title="Autocorrelation on Original Series") 
ax2 = fig.add_subplot(312)
fig = plot_acf(timeseries.diff().dropna(), ax=ax2, title="1st Order Differencing")
ax3 = fig.add_subplot(313)
fig = plot_acf(timeseries.diff().diff().dropna(), ax=ax3, title="2nd Order Differencing")


# In[39]:


plot_pacf(timeseries.diff().dropna(), lags=40) #knowing d=1 we apply diff() once
plt.show()


# In[40]:


plot_acf(timeseries.diff().dropna())
plt.show()


# In[41]:


model = ARIMA(timeseries, order=(1, 1, 0))
results = model.fit()
results.summary()


# In[42]:


graph = results.plot_predict(1, 210)
plt.title('Forecast of Confirmed -Arima model')
plt.ylabel('count')
plt.xlabel('Month')
plt.show()


# In[43]:


automodel = arimamodel(feature_mean["Confirmed"])
automodel.summary()


# In[44]:


plotarima(70, feature_mean["Confirmed"], automodel,"Confirmed")


# ## Recovered forecasting

# In[45]:


df_r=df_o.copy()


# In[46]:


s = df_r["Recovered"].isna()
indices = s[s == True].index.values.tolist()
df = df_r.drop(index=indices)
df = df_r.reset_index()


# In[47]:


features = df.select_dtypes(include=["float64"])


# In[48]:


dates = []
for i in range(0, df.shape[0], 3):
    dates.append(df["ObservationDate"][i][:10])


# In[49]:


feature_mean = pd.DataFrame(columns=features.columns, index=pd.to_datetime(dates))
for feature in features.columns:
    average = []
    for i in range(0, df.shape[0], 3):
        average.append(df[feature][i:i+3].mean())
    feature_mean[feature] = average


# In[50]:


feature_mean = feature_mean.asfreq(freq="D", method='bfill')


# In[51]:


from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# In[52]:


timeseries = feature_mean["Recovered"]


# In[53]:


print("p-value:", adfuller(timeseries.dropna())[1])


# In[54]:


fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(311)
fig = plot_acf(timeseries, ax=ax1, title="Autocorrelation on Original Series") 
ax2 = fig.add_subplot(312)
fig = plot_acf(timeseries.diff().dropna(), ax=ax2, title="1st Order Differencing")
ax3 = fig.add_subplot(313)
fig = plot_acf(timeseries.diff().diff().dropna(), ax=ax3, title="2nd Order Differencing")


# In[55]:


plot_pacf(timeseries.diff().dropna(), lags=40) #knowing d=1 we apply diff() once
plt.show()


# In[56]:


plot_acf(timeseries.diff().dropna())
plt.show()


# In[57]:


model = ARIMA(timeseries, order=(1, 1, 0))
results = model.fit()
results.summary()


# In[58]:


graph = results.plot_predict(1, 210)
plt.title('Forecast of Recovered -Arima model')
plt.ylabel('count')
plt.xlabel('Month')
plt.show()


# In[59]:


automodel = arimamodel(feature_mean["Recovered"])
automodel.summary()


# In[60]:


plotarima(70, feature_mean["Recovered"], automodel,"Recovered")


# In[ ]:




