import datetime
import json
import pandas as pd
from dateutil import parser

df = pd.read_csv('test_data.csv')
df.shape
neg=[]
pos=[]
i=j=1

for index in df.index:
    dic={}
    if df['label'][index]==-1:
        dic['id']=i
        dic['text']=df['clean_text'][index]
        date_ = df['created_at'][index]
        if isinstance(date_,str):
            date_ = datetime.datetime.strptime(date_,"%Y-%m-%dT%H:%M:%S.000Z").strftime('%Y-%m-%d')
            dic['date'] = date_
        i+=1
        neg.append(dic)
    else:
        dic['id'] = j
        dic['text'] = df['clean_text'][index]
        date_ = df['created_at'][index]
        if isinstance(date_,str):
            date_ = datetime.datetime.strptime(date_,"%Y-%m-%dT%H:%M:%S.000Z").strftime('%Y-%m-%d')
            dic['date'] = date_        
        j+=1
        pos.append(dic)


start_date =  "2015-02-28"
endDate = "2015-03-01"
for i in neg:
    print(type(start_date))
    if i['date'] >= start_date and i['date'] < endDate:
        print(i)
