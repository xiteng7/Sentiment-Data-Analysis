#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install yfinance


# In[3]:


import pandas
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import openpyxl


# In[257]:


stock_data = pd.read_excel('results of 455 videos.xlsx', sheet_name='data')
# print(stock_data)
tick = stock_data['tick'].tolist()
one_day_new = []
one_week_new = []
one_month_new = []
three_months_new = []
one_day = stock_data['1 day'].tolist()
for d in one_day:
    d_split = d.split('/')
    new_d = d_split[2]+'-'+d_split[0]+'-'+d_split[1]
    one_day_new.append(new_d)
one_week = stock_data['1 week'].tolist()
for w in one_week:
    w_split = w.split('/')
    new_w = w_split[2]+'-'+w_split[0]+'-'+w_split[1]
    one_week_new.append(new_w)
one_month = stock_data['1 month'].tolist()
for m in one_month:
    m_split = m.split('/')
    new_m = m_split[2]+'-'+m_split[0]+'-'+m_split[1]
    one_month_new.append(new_m)
three_months  = stock_data['3 months'].tolist()
for three_m in three_months:
    three_m_split = three_m.split('/')
    new_three_m = three_m_split[2]+'-'+three_m_split[0]+'-'+three_m_split[1]
    three_months_new.append(new_three_m)


# In[253]:


print(stock_data.to_string())


# In[84]:


# 7 days before published dates
last_week = stock_data['last week'].tolist()
last_week_new = []
for l_w in last_week:
    l_w_split = l_w.split('/')
    new_l_week = l_w_split[2]+'-'+l_w_split[0]+'-'+l_w_split[1]
    last_week_new.append(new_l_week)
print(last_week_new)


# In[96]:


# 30 days before published dates
last_month = stock_data['last month'].tolist()
last_month_new = []
for l_m in last_month:
    l_m_split = l_m.split('/')
    new_l_month = l_m_split[2]+'-'+l_m_split[0]+'-'+l_m_split[1]
    last_month_new.append(new_l_month)
print(last_month_new)
print(len(last_month_new))


# In[251]:


print(stock_data['date'].tolist())


# In[258]:


#videos published dates
publish_new=[]
publish_dates = stock_data['date'].tolist()
for p in publish_dates:
    p_split = p.split('/')
    new_p = p_split[2]+'-'+p_split[0]+'-'+p_split[1]
    publish_new.append(new_p)
print(publish_new)
print(len(publish_new))


# In[6]:


print(one_day_new)


# In[48]:


print(one_week_new)
print(len(one_week_new))


# In[9]:


print(one_month_new)


# In[10]:


print(three_months_new)


# In[79]:


print(tick)


# In[80]:


print(len(tick))


# In[7]:


def next_trading_day(s):
    date = datetime.strptime(str(s), "%Y-%m-%d")
    modified_date = date + timedelta(days=1)
    datetime.strftime(modified_date, "%Y-%m-%d")
    return modified_date.date()


# In[254]:


print(next_trading_day('2020-06-24'))


# In[20]:


one_day_empty = []
for i, j in zip(tick, one_day_new):
    data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    while data.empty:
        j = next_trading_day(j)
        data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    one_day_empty.append(j)


# In[14]:


print(one_day_empty)
print(len(one_day_empty))


# In[15]:


one_day_final = []
for i in one_day_empty:
    one_day_final.append(str(i))
print(one_day_final)


# In[37]:


one_day_price_list = []
for i,j in zip(tick, one_day_final):
    one_day_price = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close'][0]
    one_day_price_list.append(one_day_price)
# print(one_day_price_list)
print(len(one_day_price_list))
d = {'Dates': one_day_final, 'Prices': one_day_price_list}
df_one_day = pd.DataFrame(d)
print(df_one_day)


# In[42]:


dates_empty = []
def clean_dates(symbols, dates):
    for i, j in zip(symbols, dates):
        data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
        while data.empty:
            j = next_trading_day(j)
            data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
        dates_empty.append(str(j))
    return dates_empty


# In[49]:


dates_empty = []
week = clean_dates(tick, one_week_new)


# In[50]:


print(len(week))
print(week)


# In[52]:


one_week_price_list = []
for i,j in zip(tick, week):
    one_week_price = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close'][0]
    one_week_price_list.append(one_week_price)
print(len(one_week_price_list))
d_week = {'Dates': week, 'Prices': one_week_price_list}
df_one_week = pd.DataFrame(d_week)
print(df_one_week)


# In[53]:


dates_empty = []
month = clean_dates(tick, one_month_new)


# In[54]:


one_month_price_list = []
for i,j in zip(tick, month):
    one_month_price = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close'][0]
    one_month_price_list.append(one_month_price)
print(len(one_month_price_list))
d_month = {'Dates': month, 'Prices': one_month_price_list}
df_one_month = pd.DataFrame(d_month)
print(df_one_month)


# In[58]:


dates_empty = []
threemonths = clean_dates(tick, three_months_new)


# In[59]:


three_month_price_list = []
for i,j in zip(tick, threemonths):
    three_month_price = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close'][0]
    three_month_price_list.append(three_month_price)
print(len(three_month_price_list))
d_three_month = {'Dates': threemonths, 'Prices': three_month_price_list}
df_three_month = pd.DataFrame(d_three_month)
print(df_three_month)


# In[8]:


def previous_trading_day(p):
    date = datetime.strptime(str(p), "%Y-%m-%d")
    modified_date = date - timedelta(days=1)
    datetime.strftime(modified_date, "%Y-%m-%d")
    return modified_date.date()


# In[20]:


print(previous_trading_day('2020-04-10'))


# In[75]:


# get last trading dates before the published dates
dates_empty = []
for i, j in zip(tick, publish_new):
    data = yf.download(i, start=previous_trading_day(j), end=j, progress=False)['Close']
    while data.empty:
        j = previous_trading_day(j)
        data = yf.download(i, start=previous_trading_day(j), end=j, progress=False)['Close']
    dates_empty.append(str(previous_trading_day(j)))


# In[260]:


# get next trading dates after the published dates
# to inlcude the effects of the published videos
dates_next_trading = []
for i, j in zip(tick, publish_new):
    data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    while data.empty:
        j = next_trading_day(j)
        data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    dates_next_trading.append(str(j))


# In[249]:


print(dates_next_trading)
print(len(dates_next_trading))


# In[19]:


test = yf.download('FTV', start = '2020-04-05', end = '2020-04-13')
print(test)


# In[94]:


date  = '2021-05-28'
data = yf.download('OGN', start = '2021-05-05', end = '2021-05-20', progress  = False)['Close']
print(data)


# In[86]:


# previous trading dates of last_week_new
dates_lw = []
for i, j in zip(tick, last_week_new):
    data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    while data.empty:
        j = previous_trading_day(j)
        data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    dates_lw.append(str(j))
    print(data)
#     print(i,j)


# In[87]:


print(dates_lw)
print(len(dates_lw))


# In[98]:


# previous trading dates of last_month_new
dates_lm = []
for i, j in zip(tick, last_month_new):
    data_m = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    while data_m.empty:
        j = previous_trading_day(j)
        data_m = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    dates_lm.append(str(j))
    print(data_m)
#     print(i,j)


# In[99]:


print(dates_lm)
print(len(dates_lm))


# In[72]:


print(dates_empty)
print(len(dates_empty))


# In[73]:


previous_price_list = []
for i,j in zip(tick, dates_empty):
    previous_price = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close'][0]
    previous_price_list.append(previous_price)
print(len(previous_price_list))
d_previous = {'Dates': dates_empty, 'Prices': previous_price_list}
df_previous = pd.DataFrame(d_previous)
print(df_previous)


# In[89]:


# get a dataframe of dates and trading price on that day
#  dates are called from dates_lw which are the previous trading dates of last_week_new
lw_price_list = []
for i,j in zip(tick, dates_lw):
    lw_price = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close'][0]
    lw_price_list.append(lw_price)
print(len(lw_price_list))
d_lw_price = {'Dates': dates_lw, 'Prices': lw_price_list}
df_lw_price = pd.DataFrame(d_lw_price)
print(df_lw_price)


# In[100]:


# get a dataframe of dates and trading price on that day
#  dates are called from dates_lw which are the previous trading dates of last_month_new
lm_price_list = []
for i,j in zip(tick, dates_lm):
    lm_price = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close'][0]
    lm_price_list.append(lm_price)
print(len(lm_price_list))
d_lm_price = {'Dates': dates_lm, 'Prices': lm_price_list}
df_lm_price = pd.DataFrame(d_lm_price)
print(df_lm_price)


# In[104]:


# previous trading dates of published dates
dates_published = []
for i, j in zip(tick, publish_new):
    data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    while data.empty:
        j = previous_trading_day(j)
        data = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close']
    dates_published.append(str(j))
    print(data)
#     print(i,j)


# In[107]:


# get a dataframe of dates and trading price on that day
# dates are called from dates_lw which are the previous trading dates of published dates
# get open price 
published_price_list = []
for i,j in zip(tick, dates_published):
    pub_price = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Open'][0]
    published_price_list.append(pub_price)
print(len(published_price_list))
d_pub_price = {'Dates': dates_published, 'Open': published_price_list}
df_pub_open = pd.DataFrame(d_pub_price)
print(df_pub_open)


# In[108]:


# get a dataframe of dates and trading price on that day
#  dates are called from dates_lw which are the previous trading dates of published dates
# get close price
published_price_list = []
for i,j in zip(tick, dates_published):
    pub_price = yf.download(i, start=j, end=next_trading_day(j), progress=False)['Close'][0]
    published_price_list.append(pub_price)
print(len(published_price_list))
d_pub_price = {'Dates': dates_published, 'Close': published_price_list}
df_pub_close = pd.DataFrame(d_pub_price)
print(df_pub_close)


# In[111]:


with pd.ExcelWriter('price data.xlsx') as writer:
    df_lw_price.to_excel(writer, sheet_name = 'last_week_price')
    df_lm_price.to_excel(writer, sheet_name = 'last_month_price')
    df_pub_open.to_excel(writer, sheet_name = 'open price')
    df_pub_close.to_excel(writer, sheet_name = 'close price')


# In[76]:


with pd.ExcelWriter('price data.xlsx') as writer:
    df_previous.to_excel(writer, sheet_name='previous price')
    df_one_day.to_excel(writer, sheet_name='next day price')
    df_one_week.to_excel(writer, sheet_name='next week price')
    df_one_month.to_excel(writer, sheet_name='next month price')
    df_three_month.to_excel(writer, sheet_name='next three months price')


# In[141]:


# -------------------------------------------------------------------------


# In[112]:


pip install yahoo_fin


# In[144]:


# yahoo_fin is used to get stock fundamentals and ratios
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_financials


# In[119]:


pip install yahoofinancials


# In[162]:


from yahoofinancials import YahooFinancials
data = YahooFinancials('nflx')
income_stat = data.get_financial_stmts(frequency = 'quarterly', statement_type = 
'income')
print(income_stat['incomeStatementHistoryQuarterly']['NFLX'])


# In[158]:


count = 0
for t in tick:
    balance_stat = YahooFinancials(t).get_financial_stmts(frequency = 'quarterly', statement_type = 'balance')
    print(balance_stat['balanceSheetHistoryQuarterly'][t][0]['2018-03-31']['totalAssets'])
    count = count+1


# In[246]:


# fama french
factors_data = pd.read_excel('Fama French 4 factors.xlsx', sheet_name='Fama French 4 factors')
factors_data['Dates'] = pd.to_datetime(factors_data['Dates'].astype(str), format='%Y%m%d')
factors_data = factors_data.astype({'Dates':'string'})
print(factors_data)


# In[183]:


# create a df with published dates and ticks
df_stocks_dates = pd.DataFrame({'Dates':publish_new, 'Tickers':tick})
print(df_stocks_dates.to_string())


# In[261]:


# create a df with next trading dates and ticks
df_stocks_next_trading_dates = pd.DataFrame({'Dates':dates_next_trading, 'Tickers':tick})
print(df_stocks_next_trading_dates.to_string())


# In[238]:


print(type(df_stocks_next_trading_dates['Dates'][3]))
print(type(factors_data['Dates'][4]))


# In[262]:


combined_df = pd.merge(df_stocks_next_trading_dates, factors_data, on="Dates")
print(combined_df.to_string())


# In[263]:


with pd.ExcelWriter('famafrench.xlsx') as writer:
    combined_df.to_excel(writer, sheet_name='famafrench')


# In[179]:


modified_dates = []
for p in publish_new:
    modified_dates.append(int(p.replace('-','')))
print(modified_dates)


# In[181]:


sub_fd = factors_data[factors_data['Dates'].isin(modified_dates)]
print(sub_fd.to_string())

