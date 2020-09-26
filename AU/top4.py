# coding: utf-8

get_ipython().system('ls')
import pandas as pd
df = pd.read_excel('AUstopOut0911.xlsx')
get_ipython().system('ls')
df = pd.read_excel('AUnstopOut0911.xlsx')
df.head()
df.columns()
df.columns
for i in range(3,13):
    col = f'TextTopic13_raw{i}'
    
dfs = []
for i in range(3,13):
    col = f'TextTopic13_raw{i}'
    dfx = df[['content',col]].sort_values(col,acsending=False)
    dfx['topic'] =  i
    dfs.append(dfx)
    
for i in range(3,13):
    col = f'TextTopic13_raw{i}'
    dfx = df[['content',col]].sort_values(col,ascending=False)
    dfx['topic'] =  i
    dfs.append(dfx)
    
dfs
dfs = []
for i in range(3,13):
    col = f'TextTopic13_raw{i}'
    dfx = df[['content',col]].sort_values(col,ascending=False)[:3]
    dfx['topic'] =  i
    dfs.append(dfx)
    
dfs
for i in range(3,13):
    col = f'TextTopic13_raw{i}'
    dfx = df[['content',col]].sort_values(col,ascending=False)[:4]
    dfx['topic'] =  i
    dfs.append(dfx)
    
dfs
dfall = pd.concat(dfs)
dfall.to_csv('top4.csv')
