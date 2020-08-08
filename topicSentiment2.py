import pandas as pd

df= pd.read_excel("newTopic1.xlsx")

df['quarter'] =df['datetime'].dt.to_period('Q')

sentiment1 = df.groupby(['quarter','MainTopic']).agg({'wordscount':'sum','sentimentP1HV':'sum'}).reset_index()

sentiment1['sentimentScore'] = sentiment1['sentimentP1HV']/sentiment1['wordscount']

sentiment1City = df.groupby(['quarter','city','MainTopic']).agg({'wordscount':'sum','sentimentP1HV':'sum'}).reset_index()

sentiment1City['sentimentScore'] = sentiment1City['sentimentP1HV']/sentiment1City['wordscount']


topicweights = df.loc[:,['1 Economy outlook', '2 Government policy', '3 Construction',
       '4 Housing affordability', '5 Property size and features',
       '6 Economy outlook  Local', '7 Real estate  agent',
       '8 Housing sales activities']]

weightedPostiveWordsBase = topicweights.mul(df['sentimentP1HV'], axis=0)
weightedPostiveWordsBase['quarter'] = df['quarter']
weightedPostiveWordsBase2 = topicweights.mul(df['wordscount'], axis=0)
weightedPostiveWordsBase2['quarter'] = df['quarter']

weightedPostiveWords = pd.melt(weightedPostiveWordsBase,id_vars=['quarter'],value_vars=['1 Economy outlook', '2 Government policy', '3 Construction',
       '4 Housing affordability', '5 Property size and features',
       '6 Economy outlook  Local', '7 Real estate  agent',
       '8 Housing sales activities'], var_name='MainTopic',value_name='sentimentP1HV')

weightedWords = pd.melt(weightedPostiveWordsBase2,id_vars=['quarter'],value_vars=['1 Economy outlook', '2 Government policy', '3 Construction',
       '4 Housing affordability', '5 Property size and features',
       '6 Economy outlook  Local', '7 Real estate  agent',
       '8 Housing sales activities'], var_name='MainTopic',value_name='wordscount')

weightedPostiveWords = weightedPostiveWords.groupby(['quarter','MainTopic']).sum().reset_index()
weightedWords = weightedWords.groupby(['quarter','MainTopic']).sum().reset_index()


# sentiment2 = sentiment1[['quarter', 'MainTopic', 'wordscount']].merge(weightedPostiveWords, on=['quarter', 'MainTopic'])
sentiment2 = weightedWords.merge(weightedPostiveWords, on=['quarter','MainTopic'])


sentiment2['sentimentScore'] = sentiment2['sentimentP1HV']/sentiment2['wordscount']


weightedPostiveWordsCity = topicweights.mul(df['sentimentP1HV'], axis=0)
weightedPostiveWordsCity['quarter'] = df['quarter']
weightedPostiveWordsCity['city'] = df['city']

weightedWordsCity = topicweights.mul(df['wordscount'], axis=0)
weightedWordsCity['quarter'] = df['quarter']
weightedWordsCity['city'] = df['city']

weightedPostiveWordsCity = pd.melt(weightedPostiveWordsCity,id_vars=['quarter','city'],value_vars=['1 Economy outlook', '2 Government policy', '3 Construction',  '4 Housing affordability', '5 Property size and features',   '6 Economy outlook  Local', '7 Real estate  agent', '8 Housing sales activities'], var_name='MainTopic',value_name='sentimentP1HV')
weightedPostiveWordsCity = weightedPostiveWordsCity.groupby(['quarter','city','MainTopic']).sum().reset_index()

weightedWordsCity = pd.melt(weightedWordsCity,id_vars=['quarter','city'],value_vars=['1 Economy outlook', '2 Government policy', '3 Construction',
       '4 Housing affordability', '5 Property size and features',
       '6 Economy outlook  Local', '7 Real estate  agent',
       '8 Housing sales activities'], var_name='MainTopic',value_name='wordscount')
weightedWordsCity = weightedWordsCity.groupby(['quarter','MainTopic','city']).sum().reset_index()

# cityWords = df.groupby(['quarter', 'city']).sum()['wordscount'].reset_index()
# sentiment2City = sentiment1City[['quarter', 'city','MainTopic', 'wordscount']].merge(weightedPostiveWordsCity, on=['quarter', 'city','MainTopic'])
sentiment2City = weightedWordsCity.merge(weightedPostiveWordsCity, on=['quarter', 'city','MainTopic'])
sentiment2City['sentimentScore'] = sentiment2City['sentimentP1HV']/sentiment2City['wordscount']

with pd.ExcelWriter('TopicSentimentScores.xlsx') as w:
    sentiment1.to_excel(w, 'TopicSentiment(MainTopic)', index=0)
    sentiment1City.to_excel(w, 'TopicCitySentiment(MainTopic)',index=0)
    sentiment2.to_excel(w, 'TopicSentiment(WeightedTopic)',index=0)
    sentiment2City.to_excel(w, 'TopicCitySenti(WeightedTopic)',index=0)
    df.to_excel(w, 'rawData', index=0)

