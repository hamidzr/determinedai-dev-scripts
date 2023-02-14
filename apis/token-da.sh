#!/bin/bash -e

# get a determined token

url=$1
host=""

if [ ! -z $url ]; then
  host=$(echo $url | grep -Eo 'https?://[^/]+')
elif [ ! -z $DET_MASTER ]; then
  host=${DET_MASTER}
else
  host=http://localhost:8080
fi

  # --data-binary '{"username":"admin","password":""}' \
# check the username and password below
response=$(curl -s "${host}/api/v1/auth/login?cookie=true&isHashed=false" \
  -H 'Content-Type: application/json' \
  --data-binary '{"username":"admin","password":""}' \
  --compressed)

# token=$(echo "${response}" | jq '.token')
# if you don't have jq
token=$(echo "${response}" | grep -m 1 -o 'v2[^"]*')

echo $token
