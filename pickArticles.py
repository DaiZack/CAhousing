import pandas as pd
import string, random

df = pd.read_excel('HousingDetailsTopics.xlsx')

df['newTopic3'] = df.apply(lambda x: max(x['TextTopic_raw3'],x['TextTopic_raw4'],x['TextTopic_raw5']), axis=1)


df['newTopic1'] = df['TextTopic_raw1']
df['newTopic2'] = df['TextTopic_raw2']
df['newTopic4'] = df['TextTopic_raw6']
df['newTopic5'] = df['TextTopic_raw7']
df['newTopic6'] = df['TextTopic_raw8']
df['newTopic7'] = df['TextTopic_raw9']
df['newTopic8'] = df['TextTopic_raw10']



dfrecords = pd.DataFrame()

names = [t for t in string.ascii_letters[:24]]
random.shuffle(names)

for i in range(1,9):
    top3index = df.sort_values(f'newTopic{i}',ascending=False).drop_duplicates(subset='title')[:3].index
    top3 = df.loc[top3index,['content','title']]
    top3['filename'] = names[:3]
    names = names[3:]
    top3['topic'] = i
    for n in top3.index:
        name = top3.loc[n,'filename']
        with open(f'top3Articles/{name}.txt','w') as tp:
            tp.write(top3.loc[n,'content'])
    dfrecords = pd.concat([dfrecords,top3])

df.to_excel('newTopic1.xlsx', index=0)
dfrecords.to_csv('top3list1.csv', index=0)

