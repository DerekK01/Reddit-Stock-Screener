import pandas as pd
from datetime import date
tesla = {}
for i in range(1,31):
    date = '2021_11_' + str(i)
    df = pd.read_csv('TestData/Reddit Raw Data/mention_'+date+'.csv')
    #tesla.append(int(df.loc[df['Stock'] == 'TSLA']['Num_of_mention']))
    #tesla[date] =  int(df.loc[df['Stock'] == 'TSLA']['Num_of_mention'])
    print(df.loc[df['Stock'] == 'TSLA'])


#tesla_df = pd.DataFrame.from_dict(tesla, orient='index',columns=["Mention"])
#print(tesla_df)


