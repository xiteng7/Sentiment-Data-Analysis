#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import os


# In[4]:


os.chdir("/Users/xiteng/Desktop/Tony's Research")


# In[134]:


df = pd.read_excel(io='data analysis sheet.xlsx', sheet_name='full video')


# In[135]:


print(df)


# In[136]:


df_fear = df.loc[df['emotion'] == 'fear']
df_angry = df.loc[df['emotion'] == 'angry']
df_happy = df.loc[df['emotion'] == 'happy']
df_sad = df.loc[df['emotion'] == 'sad']


# In[137]:


print(df_fear)
print(df_angry)
print(df_happy)
print(df_sad)


# In[151]:


a = df_sad.groupby('sector')['one day return'].mean()
b = df_sad.groupby('sector')['one week return'].mean()
c = df_sad.groupby('sector')['one month return'].mean()
d = df_sad.groupby('sector')['three months return'].mean()


# In[152]:


df2 = pd.DataFrame({'one day return':a,'one week return':b,'one month return':c,'three months return':d})
print(df2)
df2.to_excel('sector_mean_return_sad.xlsx', index = True)


# In[59]:


pip install yahooquery


# In[60]:


from yahooquery import Ticker


# In[128]:


tickers = df['name'].values
print(tickers)
print(len(tickers))


# In[129]:


l_ticks = []
l_sectors = []


# In[130]:


for i in tickers:
    ticks = Ticker(i).asset_profile
    try:
        l_sectors.append(ticks[i]['sector'])
        l_ticks.append(i)
#         print(i+':',ticks[i]['sector'])
    except:
        continue
print(l_ticks)
print(l_sectors)


# In[131]:


print(len(l_sectors))
print(len(l_ticks))


# In[132]:


df_sector = pd.DataFrame({'name':l_ticks, 'sector':l_sectors})


# In[133]:


df_sector.to_excel('sector.xlsx', index = True)

