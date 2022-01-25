#!/bin/bash

# curl determined with authentication already covered

url=$1

if [ -z $DET_MASTER ]; then
  token=$(token-da.sh $url)
else
  token=$(token-da.sh)
fi


[ -z $token ] && echo "failed to get token. set var DET_MASTER." && exit 1

# -H "Content-type: application/json" \
# -H "Content-Type: application/merge-patch+json" \

curl -H "Authorization: Bearer ${token}" \
  "${@}"
