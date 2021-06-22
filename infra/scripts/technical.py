import pandas as pd
from pathlib import Path
import csv
import time
from datetime import date
import sys
import logging

startTime = time.time()

#Init Variables
inputDirectory = '/tmp/blablacar/input/'
inputFile = 'echantillon.csv'
outputDirectory = '/tmp/blablacar/output/'
numHeaders = 5
workingDate = ''
try:
    workingDate = sys.argv[1]
except ValueError:
    print(ValueError)
#workingDate = '09/06/2021'
print('workingDate')
print(workingDate)
dimCurrencyOutputFile = 'dim_currency.csv'
factExchangeRateHistoryOutputFile = 'fact_exchange_rate_history.csv'
params_headers = ['Titre', 'CodeSerie', 'Unite', 'Magnitude', 'MethodeObservation']

#Read file source
df = pd.read_csv(inputDirectory + inputFile, sep=';', header=None)

#Get Parameter DataFrame from raw DataFrame
def get_params_df(df):
    params_df = df.head(numHeaders)
    return params_df

#Clean and transpose Parameters Dataframe
def get_currencies_df(params_df, params_columns):
    clean_df = params_df.transpose()
    clean_df = clean_df[1:] 
    clean_df.columns = params_columns
    clean_df.insert(0, "currency_code", clean_df['Unite'].str.extract(r'(?<=\()(\w+)(?=\))'))
    return clean_df

#Get Parameters Dataset
params_df = get_params_df(df)
currencies_df = get_currencies_df(params_df, params_headers)

#print('params_df')
#print(params_df.iloc[:, 0:8])

#print('currencies_df.head(3)')
#print(currencies_df.head(3))

#Get Data Dataframe removing the parameters rows
data = df[numHeaders+1:]

#Get only data from date in argument if specified
if workingDate:
    data = data.loc[data[0] == workingDate]

# End script if no data recovered
if data.empty:
    print('No Data for date %s' % workingDate)
    quit()

#Clean data Dataframe
data.reset_index(drop=True, inplace=True)
data = data.apply(lambda x: x.str.replace(',','.'))
data[0] = pd.to_datetime(data[0], format='%d/%m/%Y')

#print('data')
#print(data)

#Create working dataFrame 
workingDataFrame = pd.DataFrame(columns=['updated_date', 'currency_code', 'one_euro_value' ])
#print(workingDataFrame)

#Create temporary variables
frames = []
tempRow = pd.DataFrame(columns=['one_euro_value'])
currencyFrames = []

#Clean data dataFrame 
#Enrich with params dataFrame
for index, column in enumerate(data.columns):
    if(index > 0):
        data[column] = pd.to_numeric(data[column], downcast="float")
        frames.append(data[column])
        currencyDataFrame = pd.DataFrame(columns=['currency_code'])
        currency_code_value = currencies_df['currency_code'].values[index-1]
        currencyDataFrame['currency_code'] = [currency_code_value] * len(data.index)
        currencyFrames.append(currencyDataFrame)

#Union exchangeRates values in a single column
tempRow = pd.concat(frames)
tempRow.reset_index(drop=True, inplace=True)

#Union currencyFrames values (replicated) in a single column
tempCurrencies= pd.concat(currencyFrames)
tempCurrencies.reset_index(drop=True, inplace=True)
#print('tempRow')
#print(tempRow)

#Create workingDataFrame
#Replicate date values to complete updated_date column
workingDataFrame['updated_date'] = pd.concat([data[0]]*(len(data.columns)-1), ignore_index=True)
workingDataFrame['one_euro_value'] = tempRow
workingDataFrame['currency_code'] = tempCurrencies

#print('workingDataFrame')
#print(workingDataFrame)

###############################

#Create dataframe to recover the max date for each currency
maxDateFrame = workingDataFrame[["updated_date", "currency_code"]]

#Get max date & group by currency code
maxDateFrame = maxDateFrame.groupby("currency_code").max()
maxDateFrame = maxDateFrame.reset_index()

#print('maxDateFrame')
#print(maxDateFrame)

#Get the rows in workingDataFrame having the max date
last_updated_data_df = pd.merge(workingDataFrame, maxDateFrame, on=["currency_code", "updated_date"])

# Create dim_currency dataFrame
# Enrich max date data with currencies dataFrame 
dim_currency_df = pd.merge(last_updated_data_df, currencies_df, on=["currency_code"])
dim_currency_df = dim_currency_df[["currency_code", "one_euro_value", "updated_date", "CodeSerie"]]
dim_currency_df.columns = ['cur_code', 'one_euro_value', 'last_updated_date', 'Serial_code']

print()
print('dim_currency_df total rows: %s' % (len(dim_currency_df.index)))
print()

print(dim_currency_df)

###############################

#Create exchange_rate_data by copying the data dataFrame and removing the first column (history_date)
exchange_rate_data = data.copy()
exchange_rate_data = exchange_rate_data.iloc[: , 1:]

#print('exchange_rate_data')
#print(exchange_rate_data)

#Create fact_exchange_rate_history dataFrame 
fact_exchange_rate_history = pd.DataFrame(columns=['history_date', 'from_cur_code', 'to_cur_code', 'exchange_rate'])

#Get all the exchange rates by combining each currency with the rest of them 
""" 
The innermost loop always takes time O(n), because it loops n times regardless of the values of j and i.
When the second loop runs, it runs for O(n) iterations,
 on each iteration doing O(n) work to run the innermost loop. This takes time O(n2).
Finally, when the outer loop runs, it does O(n2) work per iteration. 
It also runs for O(log n) iterations, 
 since it runs equal to the number of times you have to divide n by two before you reach 1. 
 Consequently, the total work is O(n2 log n).
 """
for i, row in exchange_rate_data.iterrows():
    history_date = data.iat[i,0]
    for j in range(row.size):
        for k in range(row.size):
            if j != k:
                from_cur_code = currencies_df['currency_code'].iloc[j]
                to_cur_code = currencies_df['currency_code'].iloc[k]
                exchange_rate = ((exchange_rate_data.iat[i,k]) / (exchange_rate_data.iat[i,j]))
                #print('ij: %s, ik: %s' % ((exchange_rate_data.iat[i,j]), (exchange_rate_data.iat[i,k])))
                #print('from: %s to %s' % (from_cur_code, to_cur_code))
                new_row = {'history_date':history_date, 'from_cur_code':from_cur_code, 'to_cur_code':to_cur_code, 'exchange_rate':exchange_rate}
                fact_exchange_rate_history = fact_exchange_rate_history.append(new_row, ignore_index=True)

#Remove the rates with null as result due to missing values in currencies
fact_exchange_rate_history = fact_exchange_rate_history[fact_exchange_rate_history['exchange_rate'].notnull()]

print()
print('fact_exchange_rate_history total rows: %s' % (len(fact_exchange_rate_history.index)))
print()
print(fact_exchange_rate_history.head(10))

executionTime = (time.time() - startTime)

print('Execution time in seconds: ' + str(executionTime))


############################

#Get bucket folder based on the current date
today = date.today()
bucket_folder = today.strftime("%Y/%m/%d")

#Create ouput directory if not exists
outputBucket = Path(outputDirectory + '/' + bucket_folder)
outputBucket.mkdir(parents=True, exist_ok=True)

#Store results dataFrames in files 
dim_currency_df.to_csv(outputBucket / dimCurrencyOutputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)
fact_exchange_rate_history.to_csv(outputBucket / factExchangeRateHistoryOutputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)

