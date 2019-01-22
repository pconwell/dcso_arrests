[![Build Status](https://travis-ci.org/pconwell/dcso_arrests.svg?branch=master)](https://travis-ci.org/pconwell/dcso_arrests)

# dcso_arrests

## docker

### 1. Clone this repo
```
$ git clone git@github.com:pconwell/dcso_arrests.git
```

### 2. edit arrests.sh

Edit arrests.sh with your github credentials.

### 3. build and run docker image

```
$ docker build --tag=arrests .
$ docker run --rm -e GITHUB_USER=user -e GITHUB_KEY=token arrests
```

### 4. (optional) Run docker image as cron

run the docker image as a crontab so that the information is updated once per day at 0630 (or whatever time)

`30 6 * * * docker run --rm -e GITHUB_USER=user -e GITHUB_KEY=token --volume "/home/pconwell/dcso_arrests/:/data" arrests`



#### Note on GITHUB token
This will depend on your specific setup, but if you follow the instructions here and your repo is public, you should only need 2 permissions on your key: `public_repo` and `read:public_key`.

----

> ignore everything below this for now

----



## Intro

This is a simple script that will scrape the daily arrests in Nashville, TN (Davidson County Sheriffs Office). The data is scraped from the [DCSO website](http://dcso.nashville.gov/Search/RecentBookings). The website only shows arrests over the past 48 hours (technically the previous 2 full days and the partial current day), and there is no easy way to look up arrests older than 48 hours. This script scrapes, cleans and sorts YESTERDAYS arrests then adds them to a csv file. We can then search the csv file to potentially locate arrests from any arbitrary date for which this script was run.

This script also comes with a bash script that will automatically run the python script and upload the updated csv to github. The bash script can be scheduled with a cronjob.

## Requirements

1. Python 3
   1. pandas
   2. requests
   3. lxml
   4. beautifulsoup4
   5. os.path
2. Bash
3. jq (`sudo apt-get install jq` or `sudo yum install jq`)

## Instructions

> These insructions assume you are going to schedule a cronjob

1. Make sure you have Python3 and the requirements installed. You will also need to install jq through your OS package manager.
2. Git clone this repo
3. Edit your arrests.sh file with your github username and OTP token
4. Set up a cronjob to run arrests.sh once per day. I set mine up like `0 8 * * * python3 ...`, which will run the script at 6 am Nashville time (+/- 1 hour depending on daylight savings time).
