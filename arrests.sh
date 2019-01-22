#!/bin/bash

python3 /app/app.py

## Set your github username and token
## $1 and $2 get passed at the command line
## ./arrests.sh user key
user=$1
token=$2
ci_type=$3
repo=dcso_arrests
file=arrests.csv

echo $user
echo $TRAVIS_EVENT_TYPE

## Get the current file from github so we can check for changes
github_file='"'`curl --silent --no-buffer --request GET --user "$user:$token" https://api.github.com/repos/$user/$repo/contents/$file | jq -r '.content' | tr -d '\n'`'"'

## Get the current file's ssh hash from github so we know which file needs to be updated (if changes exist)
github_hash='"'`curl  https://api.github.com/repos/$user/$repo/contents/$file | grep sha | cut -d '"' -f4`'"'

## Create a base64 version of the current config file (to check against $github_file and also upload if there are changes)
local_file='"'`cat /app/$file | base64 | tr -d '\n'`'"'

## Check if local version is same as github version
if [ "$github_file" == "$local_file" ];

## If the versions are the same, print "true" (this isn't necessarily important, but can be output to a log, for example)
then

	echo "version are the same -- passing";

## If the versions are different, upload the new version to github
else

        if [ "$ci_type" == "cron" ];
	
	then
	
                DATA='{"message": "update", "content": '"$local_file"', "sha": '"$github_hash"'}'
                echo $DATA  | curl -X PUT -u "$user:$token" -d @- https://api.github.com/repos/$user/$repo/contents/$file
	
	else
	        
		echo "skipping to prevent infinite loop in CI";
		
        fi

fi

