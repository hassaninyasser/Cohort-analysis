#!/usr/bin/env python
# coding: utf-8

# # Cohort analysis 

# In[14]:


import pandas as pd


# In[15]:


data=pd.read_csv('1.csv')
print(data.head())


# In[16]:


#missing value
missing_values = data.isnull().sum()
print(missing_values)


# In[17]:


#convert 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')


# In[18]:


data.info()


# In[19]:


#Descriptive statistics
data.describe()


# In[20]:


pip install plotly==5.18.0


# # look at the trend of the new and returning users over time

# In[21]:


import plotly.graph_objects as go
import plotly.express as px

import plotly.io as pio
pio.templates.default = "plotly_white"

# Trend analysis for new and returning users
fig = go.Figure()

# New Users
fig.add_trace(go.Scatter(x=data['Date'], y=data['New users'], mode='lines+markers', name='New Users'))

# Returning Users
fig.add_trace(go.Scatter(x=data['Date'], y=data['Returning users'], mode='lines+markers', name='Returning Users'))

# Update layout
fig.update_layout(title='Trend of New and Returning users over time' ,
                  xaxis_title='Data' ,
                  yaxis_title='number of users')
fig.show()


# # look at the trend of duration over time

# In[22]:


import plotly.express as px
fig = px.line(data_frame=data, x='Date', y=['Duration Day 1', 'Duration Day 7'], markers=True, labels={'value': 'Duration'})
fig.update_layout(title='Trend of Duration (Day 1 and Day 7) Over Time', xaxis_title='Date', yaxis_title='Duration', xaxis=dict(tickangle=-45))
fig.show()


# # correlation between the variables

# In[23]:


pip install seaborn


# In[24]:


import seaborn as sns
import matplotlib.pyplot as plt

# Correlation matrix
Correlation_matrix = data.corr(numeric_only=False)

# Plotting the correlation matrix
plt.figure(figsize=(9, 11))
sns.heatmap(Correlation_matrix, annot=True, cmap='coolwarm', linewidth=1 , fmt=".2f")
plt.title('Correlation Matrix of Variables')
plt.show()


# # group the data

# In[25]:


# Grouping data by week
data['Week'] = data['Date'].dt.isocalendar().week

# Calculating weekly averages
weekly_averages = data.groupby('Week').agg({
    'New users': 'mean',
    'Returning users': 'mean',
    'Duration Day 1': 'mean',
    'Duration Day 7': 'mean'
}).reset_index()

print(weekly_averages.head())


# # weekly average of the new and returning users and the duration

# In[26]:


import plotly.express as px


# In[27]:


fig1 = px.line(weekly_averages, x='Week', y=['New users', 'Returning users'], markers=True,
               labels={'value': 'Average Number of Users'}, title='Weekly Average of New vs. Returning Users')
fig1.update_xaxes(title='Week of the Year')
fig1.update_yaxes(title='Average Number of Users')

fig2 = px.line(weekly_averages, x='Week', y=['Duration Day 1', 'Duration Day 7'], markers=True,
               labels={'value': 'Average Duration'}, title='Weekly Average of Duration (Day 1 vs. Day 7)')
fig2.update_xaxes(title='Week of the Year')
fig2.update_yaxes(title='Average Duration')

fig1.show()
fig2.show()


# # create a cohort chart to understand the cohort matrix of weekly averages

# In[33]:


# Creating a cohort matrix
cohort_matrix = weekly_averages.set_index('Week')

# Plotting the cohort matrix
plt.figure(figsize=(11, 8))

sns.heatmap(cohort_matrix, annot=True, cmap='crest', fmt=".1f" , linewidth=1)
plt.title('Cohort Matrix of Weekly Averages')
plt.ylabel('Week of the Year')
plt.show()


# In[ ]:




