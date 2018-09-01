# dcso_arrests

## Intro

This is a simple script that will scrape the daily arrests in Nashville, TN (Davidson County Sheriffs Office). The data is scraped from the [DCSO website](http://dcso.nashville.gov/Search/RecentBookings). The website only shows arrests over the past 48 hours (technically the previous 2 full days and the partial current day). This script scrapes, cleans and sorts YESTERDAYS arrests then adds them to a csv file.

This script also comes with a bash script that will automatically run the python script and upload the updated csv to github. The bash script can be scheduled with a cronjob.

## Requirements

1. Python 3
   1. pandas
   2. requests
   3. lxml
   4. beautifulsoup4
2. Bash
3. jq (`sudo apt-get install jq` or `sudo yum install jq`)

## Instructions

> These insructions assume you are going to schedule a cronjob

1. Make sure you have Python3 and the requirements installed. You will also need to install jq through your OS package manager.
2. Git clone this repo
3. Edit your arrests.sh file with your github username and OTP token.
4. If you are starting from scratch and not using the currently existing csv, you will need to 'seed' your csv file. You can comment out the lines `with open('arrests.csv', 'a') as f: df.to_csv(f, header=False)` and uncomment `df.to_csv('./arrests.csv')` to generate the initial csv file. Once the csv file exists, make sure to reverse your changes or you will overwrite the csv file instead of append to it.
5. set up a cronjob to run arrests.sh once per day. I set mine up like `0 8 * * * python3 ...`.
