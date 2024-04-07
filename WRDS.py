#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install wrds


# In[2]:


import pandas as pd
import wrds
from datetime import datetime, timedelta
import openpyxl
import os


# In[9]:


print(os.getcwd())


# In[216]:


db = wrds.Connection(wrds_username='your_username')


# In[179]:


stock_data = pd.read_excel('data analysis on 450 videos.xlsx', sheet_name='calculated_DATA')
date_list = stock_data['last quarter'].to_list()
last_quarters = []
for i in date_list:
    j = i.split('/')
    new_date = j[2]+'-'+j[0]+'-'+j[1]
    last_quarters.append(new_date)
print(last_quarters)
print(len(last_quarters))


# In[138]:


dates = stock_data['Dates'].to_list()
print(dates)
print(len(dates))


# In[220]:


stocks = stock_data['Tickers'].to_list()
print(stocks)
print(len(stocks))


# In[217]:


def assets(start_date, end_date, ticker):
    results = db.raw_sql(f"""
        SELECT datadate, tic, atq
        FROM comp.fundq
        WHERE tic = '{ticker}'
        AND datadate >= '{start_date}' AND datadate <= '{end_date}'
        ORDER BY datadate
    """
        )
    return(results)

def sales(start_date, end_date, ticker):
    results = db.raw_sql(f"""
        SELECT datadate, tic, SALEQ
        FROM comp.fundq
        WHERE tic = '{ticker}'
        AND datadate >= '{start_date}' AND datadate <= '{end_date}'
        ORDER BY datadate
    """
        )
    return(results)

def net_income(start_date, end_date, ticker):
    results = db.raw_sql(f"""
        SELECT datadate, tic, CIBEGNIQ
        FROM comp.fundq
        WHERE tic = '{ticker}'
        AND datadate >= '{start_date}' AND datadate <= '{end_date}'
        ORDER BY datadate
    """
        )
    return(results)

def shares(start_date, end_date, ticker):
    results = db.raw_sql(f"""
        SELECT datadate, tic, CSHPRQ
        FROM comp.fundq
        WHERE tic = '{ticker}'
        AND datadate >= '{start_date}' AND datadate <= '{end_date}'
        ORDER BY datadate
    """
        )
    return(results)


# In[229]:


# assets
assets_df = pd.DataFrame(columns=['datadate', 'tic', 'atq'])
for i, j, k in zip(last_quaters, dates, stocks):
    data_to_append = assets(i, j, k)
    print(i,j,k)
    assets_df = pd.concat([assets_df, data_to_append], axis=0, ignore_index=True)


# In[230]:


print(assets_df.to_string())


# In[168]:


# sales
sales_df = pd.DataFrame(columns=['datadate', 'tic', 'saleq'])
for i, j, k in zip(last_quaters, dates, stocks):
    data_to_append = sales(i, j, k)
    sales_df = sales_df.append(data_to_append, ignore_index=True)


# In[169]:


print(sales_df)


# In[170]:


# net income
income_df = pd.DataFrame(columns=['datadate', 'tic', 'cibegniq'])
for i, j, k in zip(last_quaters, dates, stocks):
    data_to_append = net_income(i, j, k)
    income_df = income_df.append(data_to_append, ignore_index=True)


# In[171]:


print(income_df)


# In[173]:


# shares
shares_df = pd.DataFrame(columns=['datadate', 'tic', 'cshprq'])
for i, j, k in zip(last_quaters, dates, stocks):
    data_to_append = shares(i, j, k)
    shares_df = shares_df.append(data_to_append, ignore_index=True)


# In[174]:


print(shares_df)


# In[178]:


last_two_quarters = []
for i in stock_data['last two quarters'].to_list():
    j = i.split('/')
    new_date = j[2]+'-'+j[0]+'-'+j[1]
    last_two_quarters.append(new_date)
print(last_two_quarters)
print(len(last_two_quarters))


# In[180]:


# last quarter sales
last_sales_df = pd.DataFrame(columns=['datadate', 'tic', 'saleq'])
for i, j, k in zip(last_two_quarters, last_quarters, stocks):
    data_to_append = sales(i, j, k)
    last_sales_df = last_sales_df.append(data_to_append, ignore_index=True)


# In[181]:


print(last_sales_df)


# In[183]:


# last quarter net income
last_income_df = pd.DataFrame(columns=['datadate', 'tic', 'cibegniq'])
for i, j, k in zip(last_two_quarters, last_quarters, stocks):
    data_to_append = net_income(i, j, k)
    last_income_df = last_income_df.append(data_to_append, ignore_index=True)


# In[184]:


print(last_income_df)


# In[188]:


def equity(start_date, end_date, ticker):
    results = db.raw_sql(f"""
        SELECT datadate, tic, TEQQ
        FROM comp.fundq
        WHERE tic = '{ticker}'
        AND datadate >= '{start_date}' AND datadate <= '{end_date}'
        ORDER BY datadate
    """
        )
    return(results)


# In[191]:


# equity
equity_df = pd.DataFrame(columns=['datadate', 'tic', 'teqq'])
for i, j, k in zip(last_quarters, dates, stocks):
    data_to_append = equity(i, j, k)
    equity_df = equity_df.append(data_to_append, ignore_index=True)


# In[192]:


print(equity_df)


# In[193]:


# last quarter equity
last_equity_df = pd.DataFrame(columns=['datadate', 'tic', 'teqq'])
for i, j, k in zip(last_two_quarters, last_quarters, stocks):
    data_to_append = equity(i, j, k)
    last_equity_df = last_equity_df.append(data_to_append, ignore_index=True)


# In[194]:


print(last_equity_df)


# In[195]:


# last quarter shares
last_shares_df = pd.DataFrame(columns=['datadate', 'tic', 'cshprq'])
for i, j, k in zip(last_two_quarters, last_quarters, stocks):
    data_to_append = shares(i, j, k)
    last_shares_df = last_shares_df.append(data_to_append, ignore_index=True)


# In[196]:


print(last_shares_df)


# In[232]:


with pd.ExcelWriter('fundamentals.xlsx') as writer:
    assets_df.to_excel(writer)


# In[231]:


assets('2022-03-10', '2022-06-09', 'FOX')


# In[ ]:




