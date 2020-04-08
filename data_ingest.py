import pandas as pd
import os
import numpy as np
def data_ingest():
    """
    Function to perform Data preprocessing and Filtering
    """
    path = r"data1/"
    list = os.listdir(path)
    # print(list)
    c=0
    for sheet in list:
        df = pd.read_csv(os.path.join(path,sheet),sep=",")
        df.fillna(0,inplace=True) # Filling Nan with 0

        # Combining each excel
        if c==0:
            combined_df = df #Copying first excel as it is
        else:
            combined_df['NewCol'+str(c)] = df['Value'] #Copying value columns from others
        c+=1
    combined_df.rename(columns={'Value':'Confirmed','NewCol1':'Death','NewCol2':'Recovered'},inplace=True)
    combined_df.drop(0,inplace=True)
    combined_df =  combined_df.reset_index(drop=True)
    #If no province available, fill with Country/Region
    combined_df['Location'] = np.where(combined_df['Province/State']==0,combined_df['Country/Region'] , combined_df['Province/State'])
    # print(combined_df.tail())

    #Writing to a csv file
    combined_df.to_csv(r'covid.csv',index=False,sep='\t' )

    # Creating a new dataframe with aggregate values of country
    combined_df['Date'] = pd.to_datetime(combined_df['Date']) #Converting to datetype
    for c in ['Lat','Long','Confirmed','Death','Recovered']:
        combined_df[c] = pd.to_numeric(combined_df[c], errors='coerce',downcast='integer')
    latest_date = combined_df['Date'].max() #Finding latest date

    # Copying the rows with latest date
    latest_df=combined_df.loc[combined_df.Date == latest_date].copy()
    for c in ['Lat','Long','Confirmed','Death','Recovered']:
        latest_df[c] = pd.to_numeric(latest_df[c], errors='coerce',downcast='integer')
    latest_df =  latest_df.reset_index(drop=True)
    # print(latest_df.head())
    latest_df_copy=latest_df.drop(['Province/State'],axis=1)

    aggregations = { 'Lat':'first','Long':'first','Date':'first','Confirmed':'sum','Death':'sum','Recovered':'sum'}
    country_df=latest_df_copy.groupby("Country/Region",as_index=False).agg(aggregations) #groupby Country values
    country_df.to_csv(r'countries.csv',index=False,sep='\t' )
    # print(country_df['Recovered'].sum())

    aggregations = { 'Lat':'first','Long':'first','Confirmed':'sum','Death':'sum','Recovered':'sum'}
    countryDays_df=combined_df.groupby(["Country/Region","Date"],as_index=False).agg(aggregations) #groupby Country and Date values
    print(combined_df,latest_df,country_df,countryDays_df)
    # print(countryDays_dfl;;..01})
    return combined_df,latest_df, country_df,countryDays_df
# data_ingest()
