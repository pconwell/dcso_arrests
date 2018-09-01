import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os.path

# set pandas to show all columns
pd.set_option('display.expand_frame_repr', False)

# open DCSO website for recent bookings and find the table within that website
url = "http://dcso.nashville.gov/Search/RecentBookings"
page = requests.get(url)
soup = BeautifulSoup(page.content,'lxml')
t = soup.find('table', {'id':'recent-bookings-results-list'})

# put the table into a pandas dataframe (technically creates a list of dataframes, so we will get the first item of the list)
df = pd.read_html(str(t))
df = df[0]

# clean up arrest time
df['arrest'] = pd.to_datetime(df['ADMITTED_DATE'])

# clean up control number (maybe just drop this? Not sure what it is for)
df['control'] = df['CONTROL_NUMBER'].fillna(0).astype(int)

# clean up names and split into first and last
df['last'], df['first'] = df['Inmate Name'].str.split(',', 1).str
df['first'] = df['first'].str.strip()

# separate age and clean up date
df['age'] = df['DATE_OF_BIRTH'].astype(str).str[-3:-1]
df['dob'] = pd.to_datetime(df['DATE_OF_BIRTH'].astype(str).str[:-5])

# rename some columns
df.rename(columns={'SEX': 'sex', 'RACE_DESC': 'race'}, inplace=True)

# drop the columns we don't need
df = df.drop(columns=['Details', 'RELEASE_DATE', 'ADMITTED_DATE', 'CONTROL_NUMBER', 'DATE_OF_BIRTH', 'Inmate Name'])

# subset yesterday's date (so when we append, we won't duplicate. We will only add one date at a time.)
df = df[(df['arrest'] > pd.Timestamp(datetime.datetime.today().date()) - datetime.timedelta(1)) & (df['arrest'] < pd.Timestamp(datetime.datetime.today().date()))]

# sort df by time so it's organized and pretty
df.sort_values(by=['arrest'], inplace=True)

# reset the index so that it's clean looking. Not strictly necessary, but it will make the output csv cleaner
# this will reset the index to whatever the last row number is in the existing csv file
df.reset_index(inplace=True)
df.index += pd.read_csv("./arrests.csv")['Unnamed: 0'].max() + 1

# drops the index column which gets generated from the OLD index numbers when the index is reset above
df = df.drop(columns=['index'])

# check if the csv file already exists. If not, create a new one. If it exists, append to the existing one.
if os.path.isfile('./arrests.csv') is True:
    print('file exists, appending...')
    with open('arrests.csv', 'a') as f:
        df.to_csv(f, header=False)

else:
    print('file does not exists, creating...')
    df.to_csv('./arrests.csv')

# check for travis-ci to see what data is showing up during testing
print('***** df *****')
print(df)

print('***** csv *****')
print(pd.read_csv("./arrests.csv"))
