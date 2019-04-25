import pandas_datareader.data as web
import datetime

start = datetime.datetime(2017,1,1)
end = datetime.datetime(2019,4,25)

df = web.DataReader('TSLA', 'yahoo', start, end)

print(df.head())
