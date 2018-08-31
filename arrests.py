import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

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

# clean up control number (maybe just drop this?)
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

# subset yesterday's date (so when we append, we won't duplicate. We will only add one date at a time.
df = df[(df['arrest'] > pd.Timestamp(datetime.datetime.today().date()) - datetime.timedelta(1)) & (df['arrest'] < pd.Timestamp(datetime.datetime.today().date()))]

# sort by time
df.sort_values(by=['arrest'], inplace=True)

df.reset_index(inplace=True)
df.index += pd.read_csv("./arrests.csv")['Unnamed: 0'].max() + 1

df = df.drop(columns=['index'])

print(df)

#df.to_csv('./arrests.csv')

with open('arrests.csv', 'a') as f:
    df.to_csv(f, header=False)