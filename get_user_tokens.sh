#!/usr/bin/env bash

set -o allexport
source .env
set +o allexport

TOKENS=$(curl -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0" \
  -H "Content-Type: application/x-www-form-urlencoded" -X POST -d \
  "grant_type=authorization_code" -d "client_id=${CLIENT_ID}" -d \
  "client_secret=${CLIENT_SECRET}" -d "code=${CODE}" \
  'https://hh.ru/oauth/token' | jq '.access_token + " " + .refresh_token')

TOKENS=$(echo $TOKENS | tr "\"" " ")

ACCESS_TOKEN=$(echo $TOKENS | awk '{print $1}')
REFRESH_TOKEN=$(echo $TOKENS | awk '{print $2}')

sed -i 's|HH_TOKEN=.*|HH_TOKEN='"${ACCESS_TOKEN}"'|g' .env
sed -i 's|HH_REFRESH_TOKEN=.*|HH_REFRESH_TOKEN='"${REFRESH_TOKEN}"'|g' .env
