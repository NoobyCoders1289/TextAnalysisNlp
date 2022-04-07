import datetime
import json
import pandas as pd

df = pd.read_csv('test_data.csv')
df.shape
df['date'] = pd.to_datetime(df['created_at'],format='%Y-%m-%d')
neg=[]
pos=[]
i=j=1

for index in df.index:
    dic={}
    if df['label'][index]==-1:
        dic['id']=i
        dic['text']=df['clean_text'][index]
        dat = df['created_at'][index]
        if isinstance(dat,str):
            dic['date'] = datetime.datetime.fromtimestamp(dat)
        i+=1
        neg.append(dic)
    else:
        dic['id'] = j
        dic['text'] = df['clean_text'][index]
        dat = df['created_at'][index]
        if isinstance(dat,str):
            dic['date'] = datetime.datetime.strptime(dat,"%Y-%m-%dT%H:%M:%SZ")        
        j+=1
        pos.append(dic)

print(json.dumps(neg,indent=2))