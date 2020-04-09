import pandas as pd
import os
import numpy as np
def data_ingest():
    """
    Function to perform Data preprocessing and Filtering
    """
    path = r"data2/"
    list = os.listdir(path)
    # print(list)
    c=0
    keys = ['Province/State', 'Country/Region', 'Lat', 'Long', 'Date',
        'ISO 3166-1 Alpha 3-Codes', 'Region Code', 'Sub-region Code',
       'Intermediate Region Code']
    for sheet in list:
        df = pd.read_csv(os.path.join(path,sheet),sep=",")
        df.drop(0,inplace=True)
        df = df.reset_index(drop=True)
        df.fillna(0,inplace=True) # Filling Nan with 0
        # Combining each excel
        if c==0:
            combined_df = df #Copying first excel as it is
        else:
            combined_df = pd.merge(combined_df,df,how = 'outer',on = keys)

        c+=1

    combined_df.rename(columns={'Value_x':'Confirmed','Value_y':'Death','Value':'Recovered'},inplace=True)
    combined_df['Date'] = pd.to_datetime(combined_df['Date']) #Converting to datetype
    for c in ['Lat','Long','Confirmed','Death','Recovered','Region Code','Sub-region Code','Intermediate Region Code']:
        combined_df[c] = pd.to_numeric(combined_df[c], errors='coerce',downcast='integer')
    combined_df.fillna(0,inplace=True) # Filling Nan with 0

    #If no province available, fill with Country/Region
    combined_df['Location'] = np.where(combined_df['Province/State']==0,combined_df['Country/Region'] , combined_df['Province/State'])

    # Adding Active cases field
    combined_df['Active'] = combined_df['Confirmed']-(combined_df['Death']+combined_df['Recovered'])
    combined_df['Active'] = pd.to_numeric(combined_df['Active'], errors='coerce',downcast='integer')
    # Adding Fatality field
    combined_df.loc[combined_df['Death'] == 0, 'Fatality Rate'] = 0
    combined_df.loc[combined_df['Death'] > 0, 'Fatality Rate'] = combined_df['Death']/combined_df['Confirmed']

    combined_df = combined_df.sort_values(['Country/Region','Province/State','Date'], ascending = False)
    # print(combined_df_copy)

    # combined_df_copy = combined_df_copy[['Confirmed','Active','Recovered','Death']].diff(periods=-1)
    combined_df['New Confirmed'] = combined_df.groupby(['Country/Region','Province/State'])['Confirmed'].diff(periods=-1).fillna(0)
    combined_df['New Death'] = combined_df.groupby(['Country/Region','Province/State'])['Death'].diff(periods=-1).fillna(0)
    combined_df['New Recovered'] = combined_df.groupby(['Country/Region','Province/State'])['Recovered'].diff(periods=-1).fillna(0)
    combined_df = combined_df.sort_values(['Country/Region','Province/State'], ascending = True)


    # print(combined_df)


    #Writing to a xlsx file
    combined_df.to_excel(r'combined.xlsx',index=False)

    #  Creating new df after dropping the fields that arent needed
    base_df = combined_df.drop(['ISO 3166-1 Alpha 3-Codes', 'Region Code', 'Sub-region Code',
   'Intermediate Region Code'], axis = 1)
    # Writing to csv file
    base_df.to_csv(r'covid.csv',index=False,sep='\t' )

    # Grouping by countries and Date -> Result : Countries with all days
    aggregations = { 'Lat':'first','Long':'first','Confirmed':'sum',
    'Active':'sum','Death':'sum','Recovered':'sum','Fatality Rate':'mean',
    'New Confirmed':'sum','New Death':'sum','New Recovered':'sum'}
    countryDays_df=combined_df.groupby(["Country/Region","Date"],as_index=False).agg(aggregations) #groupby Country and Date values

    # Finding the latest date
    latest_date = combined_df['Date'].max() #Finding latest date

    # Countries and provinces with latest date only
    latest_df=base_df.loc[base_df.Date == latest_date].copy()
    latest_df =  latest_df.reset_index(drop=True)

    # Creating a copy
    latest_df_copy=latest_df.drop(['Province/State'],axis=1)

    # Grouping by countries alone -> Result: Countries with latest dates
    aggregations = { 'Lat':'first','Long':'first','Confirmed':'sum','Date':'first',
    'Active':'sum','Death':'sum','Recovered':'sum','Fatality Rate':'mean',
    'New Confirmed':'sum','New Death':'sum','New Recovered':'sum'}
    countryLatest_df=latest_df_copy.groupby("Country/Region",as_index=False).agg(aggregations) #groupby Country values
    countryLatest_df.to_csv(r'countries.csv',index=False,sep='\t' )

#
    # print(combined_df,base_df,countryDays_df,latest_df, countryLatest_df.head())

    return base_df,countryDays_df,latest_df, countryLatest_df
# data_ingest()
