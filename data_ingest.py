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
    combined_df.loc[combined_df['Death'] > 0, 'Fatality Rate'] = round((combined_df['Death']/combined_df['Confirmed'])*100,2)
    combined_df.loc[combined_df['Confirmed'] == 0, 'Fatality Rate'] = 0

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
    'Active':'sum','Death':'sum','Recovered':'sum',
    'New Confirmed':'sum','New Death':'sum','New Recovered':'sum'}
    countryDays_df=combined_df.groupby(["Country/Region","Date"],as_index=False).agg(aggregations) #groupby Country and Date values

    countryDays_df.loc[countryDays_df['Death'] == 0, 'Fatality Rate'] = 0
    countryDays_df.loc[countryDays_df['Death'] > 0, 'Fatality Rate'] = round((countryDays_df['Death']/countryDays_df['Confirmed'])*100,2)
    countryDays_df.loc[countryDays_df['Confirmed'] == 0, 'Fatality Rate'] = 0
    # print(countryDays_df.isnull().sum())
    # Finding the latest date
    latest_date = combined_df['Date'].max() #Finding latest date

    # Countries and provinces with latest date only
    latest_df=base_df.loc[base_df.Date == latest_date].copy()
    latest_df =  latest_df.reset_index(drop=True)
    for c in ['Lat','Long','Confirmed','Death','Active','Recovered','New Confirmed','New Death','New Recovered']:
        latest_df[c] = pd.to_numeric(latest_df[c], errors='coerce',downcast='integer')
    latest_df.to_csv(r'latest_df.csv',index=False,sep='\t' )

    # Creating a copy
    latest_df_copy=latest_df.drop(['Province/State'],axis=1)

    # Grouping by countries alone -> Result: Countries with latest dates
    aggregations = { 'Lat':'first','Long':'first','Confirmed':'sum','Date':'first',
    'Active':'sum','Death':'sum','Recovered':'sum',
    'New Confirmed':'sum','New Death':'sum','New Recovered':'sum'}
    countryLatest_df=latest_df_copy.groupby("Country/Region",as_index=False).agg(aggregations) #groupby Country values

    countryLatest_df.loc[countryLatest_df['Death'] == 0, 'Fatality Rate'] = 0
    countryLatest_df.loc[countryLatest_df['Death'] > 0, 'Fatality Rate'] = round((countryLatest_df['Death']/countryLatest_df['Confirmed'])*100,2)
    countryLatest_df.loc[countryLatest_df['Confirmed'] == 0, 'Fatality Rate'] = 0
    # print(countryDays_df.isnull().sum())
    countryLatest_df.to_csv(r'countries.csv',index=False,sep='\t' )

    canada_df = latest_df.loc[latest_df['Country/Region'] == 'Canada']
    canada_pop = {'Province/State': ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador',
        'Northwest Territories', 'Nova Scotia', 'Ontario', 'Prince Edward Island',  'Quebec', 'Saskatchewan', 'Yukon','Nunavut'],
        'Population': [4413146, 5110917, 1377517, 779993, 521365, 44904, 977457, 14711827, 158158, 8537674, 1181666, 41078, 39097]
    }
    canada_pop_df = pd.DataFrame.from_dict(canada_pop)
    canada_df = pd.merge(canada_df,canada_pop_df,how = 'left',on = 'Province/State').fillna(0)
    # print(canada_df.dtypes)
    canada_df.loc[canada_df['Population'] == 0, 'Cases Per Population'] = 0
    canada_df.loc[canada_df['Population'] > 0, 'Cases Per Population'] = round((canada_df['Confirmed']/canada_df['Population'])*100000)

    for c in ['Population','Cases Per Population']:
        canada_df[c] = pd.to_numeric(canada_df[c], errors='coerce',downcast='integer')
    # print(canada_df)
    aggregations = {'Confirmed':'sum',
    'Active':'sum','Death':'sum','Recovered':'sum', 'New Confirmed':'sum', 'New Death':'sum', 'New Recovered':'sum', 'Fatality Rate':'mean'}
    sum_df=countryDays_df.groupby("Date",as_index=False).agg(aggregations) #groupby Date values
    sum_df.to_csv(r'sumdf.csv',index=False,sep='\t')

    # print(sum_df)

    countryDays_df.to_csv(r'countryDays_df.csv',index=False,sep='\t' )
#
#
    # print(combined_df,base_df,countryDays_df,latest_df, countryLatest_df.head())
    # print(latest_df.dtypes)
    return base_df,countryDays_df,latest_df, countryLatest_df,canada_df
# data_ingest()
