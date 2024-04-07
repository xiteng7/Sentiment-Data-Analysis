#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install yfinance


# In[115]:


pip install statsmodels


# In[1]:


import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import openpyxl
import os
import statsmodels.api as sm


# In[2]:


stock_data = pd.read_excel('results of 450 videos.xlsx', sheet_name='data')


# In[3]:


date_list = stock_data['date'].tolist()
print(date_list)


# In[4]:


year_list_start = []
for i in date_list:
    year = i.split('/')[2]
    year = str(int(year)-1)
    year = year + '-' + i.split('/')[0] + '-' + i.split('/')[1]
    year_list_start.append(year)
print(year_list_start)


# In[5]:


year_list_end = []
for i in date_list:
    year = i.split('/')[2] + '-' + i.split('/')[0] + '-' + i.split('/')[1]
    year_list_end.append(year)
print(year_list_end)


# In[6]:


tick_list = stock_data['tick'].tolist()
print(tick_list)
print(len(tick_list))


# In[82]:


df_price = yf.download("A", start= '2020-12-30', end = '2021-03-05',interval='1wk')
df_price.reset_index(inplace=True)
df_price = df_price[['Date', 'Adj Close']]
df_price['Percentage Return'] = df_price['Adj Close'].pct_change()
df_price = df_price.drop(df_price.index[0])
print(df_price)


# In[7]:


factors_data = pd.read_excel('fama_frech_daily.xlsx', sheet_name='factors data')
print(factors_data)


# In[8]:


factors_dates = factors_data['Dates'].tolist()
print(factors_dates)


# In[9]:


factors_dates_modified = []
for i in factors_dates:
    i = str(i)
    d = i[:4] + '-' + i[4:6] + '-' + i[6:8]
    factors_dates_modified.append(d)
print(factors_dates_modified)


# In[10]:


factors_data.insert(1, 'modified_dates', factors_dates_modified)


# In[11]:


cols_to_divide = ['Mkt-RF', 'SMB', 'HML', 'RF', 'Mom']
factors_data[cols_to_divide] = factors_data[cols_to_divide]/100


# In[12]:


print(factors_data)


# In[13]:


data_analysis = pd.read_excel('data analysis on 450 videos.xlsx', sheet_name='calculated_DATA')


# In[15]:


filtered_dates = data_analysis['Dates'].tolist()
print(filtered_dates)
print(len(filtered_dates))
filtered_factor_data = factors_data[factors_data['modified_dates'].isin(filtered_dates)]
print(filtered_factor_data)


# In[101]:


print(data_analysis)


# In[104]:


factors_data['mofidied_dates'] = pd.to_datetime(factors_data['mofidied_dates'])
data_analysis['Dates'] = pd.to_datetime(data_analysis['Dates'])
new_combined_df = data_analysis.merge(factors_data, left_on='Dates', right_on='mofidied_dates', how='inner')
print(new_combined_df)


# In[100]:


with pd.ExcelWriter('new_data_analysis.xlsx') as writer:
    new_combined_df.to_excel(writer)


# In[90]:


factors_data['mofidied_dates'] = pd.to_datetime(factors_data['mofidied_dates'])
combined_df = pd.concat([factors_data.set_index('mofidied_dates'), df_price.set_index('Date')], axis=1, join='inner')
print(combined_df)


# In[73]:


combined_df = df_price.merge(factors_data, left_on='Date', right_on='mofidied_dates', how='inner')
print(combined_df)


# In[31]:


X = combined_df[['SMB', 'HML', 'Mkt-RF', 'Mom']]
y = combined_df['Percentage Return'] - combined_df['RF']

# Add a constant to the independent variables matrix
X = sm.add_constant(X)

# Perform the multiple linear regression
model = sm.OLS(y, X).fit()

# Print the regression summary
print(model.summary())


# In[32]:


coefficients = model.params
print(coefficients)
print(coefficients[1])
print(coefficients[2])
print(coefficients[3])
print(coefficients[4])


# In[48]:


beta_SMB = []
beta_HML = []
beta_MktRF = []
beta_Mom = []
error_catch = []
for i, j, k in zip(tick_list, year_list_start, year_list_end):
    try:
        dfprice = yf.download(i, start= j, end = k,interval='1mo')    
        dfprice.reset_index(inplace=True)
        dfprice = dfprice[['Date', 'Adj Close']]
        # Did not use *100
        dfprice['Percentage Return'] = dfprice['Adj Close'].pct_change()
        dfprice = dfprice.drop(dfprice.index[0])
        print(dfprice)
        
        factors_data['mofidied_dates'] = pd.to_datetime(factors_data['mofidied_dates'])
        combined_df = pd.concat([factors_data.set_index('mofidied_dates'), dfprice.set_index('Date')], axis=1, join='inner')
        print(combined_df)

        X = combined_df[['SMB', 'HML', 'Mkt-RF', 'Mom']]
        y = combined_df['Percentage Return'] - combined_df['RF']
        # Add a constant to the independent variables matrix
        X = sm.add_constant(X)
        # Perform the multiple linear regression
        model = sm.OLS(y, X).fit()
        coefficients = model.params
        print(coefficients)
        beta_SMB.append(coefficients[1])
        beta_HML.append(coefficients[2])
        beta_MktRF.append(coefficients[3])
        beta_Mom.append(coefficients[4])
    except:
        error_catch.append(i)
        continue


# In[49]:


print(beta_SMB)
print(len(beta_SMB))
print(beta_HML)
print(len(beta_HML))
print(beta_MktRF)
print(len(beta_MktRF))
print(beta_Mom)
print(len(beta_Mom))
print(error_catch)
print(len(error_catch))


# In[50]:


tick_list_temp = tick_list
tick_list_temp.remove('OGN')
tick_list_temp.remove('RE')
tick_list_temp.remove('WELL')
print(tick_list_temp)
print(len(tick_list_temp))


# In[51]:


data = {
    'tick': tick_list_temp,
    'SMB': beta_SMB,
    'HML': beta_HML,
    'Mkt-RF': beta_MktRF,
    'Mom': beta_Mom
}

df_betas = pd.DataFrame(data)
print(df_betas)


# In[55]:


data_analysis = pd.read_excel('data analysis on 450 videos.xlsx', sheet_name='calculated_DATA')
print(data_analysis)


# In[56]:


combined_df2 = data_analysis.merge(df_betas, left_on='tick', right_on='tick', how='inner')
print(combined_df2)


# In[57]:


with pd.ExcelWriter('betas_daily.xlsx') as writer:
    combined_df2.to_excel(writer)


# In[53]:


# WELL
df_price = yf.download("WELL", start = '2019-02-28', end = '2020-02-29',interval='1d')
df_price.reset_index(inplace=True)
df_price = df_price[['Date', 'Adj Close']]
df_price['Percentage Return'] = df_price['Adj Close'].pct_change()
df_price = df_price.drop(df_price.index[0])
print(df_price)

factors_data['mofidied_dates'] = pd.to_datetime(factors_data['mofidied_dates'])
combined_df = pd.concat([factors_data.set_index('mofidied_dates'), df_price.set_index('Date')], axis=1, join='inner')
print(combined_df)

X = combined_df[['SMB', 'HML', 'Mkt-RF', 'Mom']]
y = combined_df['Percentage Return'] - combined_df['RF']
# Add a constant to the independent variables matrix
X = sm.add_constant(X)
# Perform the multiple linear regression
model = sm.OLS(y, X).fit()
coefficients = model.params
print(coefficients)
print(coefficients[1])
print(coefficients[2])
print(coefficients[3])
print(coefficients[4])


# In[58]:


# RE
df_price = yf.download("RE", start = '2019-02-19', end = '2020-02-19',interval='1d')
df_price.reset_index(inplace=True)
df_price = df_price[['Date', 'Adj Close']]
df_price['Percentage Return'] = df_price['Adj Close'].pct_change()
df_price = df_price.drop(df_price.index[0])
print(df_price)

factors_data['mofidied_dates'] = pd.to_datetime(factors_data['mofidied_dates'])
combined_df = pd.concat([factors_data.set_index('mofidied_dates'), df_price.set_index('Date')], axis=1, join='inner')
print(combined_df)

X = combined_df[['SMB', 'HML', 'Mkt-RF', 'Mom']]
y = combined_df['Percentage Return'] - combined_df['RF']
# Add a constant to the independent variables matrix
X = sm.add_constant(X)
# Perform the multiple linear regression
model = sm.OLS(y, X).fit()
coefficients = model.params
print(coefficients)
print(coefficients[1])
print(coefficients[2])
print(coefficients[3])
print(coefficients[4])


# In[197]:


# stock OGN does not have enought data points 

