#!/bin/bash

CLIENT_ID=<необходимо заполнить значениями, выданными при регистрации приложения>
CLIENT_SECRET=<необходимо заполнить значениями, выданными при регистрации приложения>
CODE=<значение authorization_code, полученное при логине https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}>

curl -H "User-Agent: test-api/1.0 (feedback@botayhard.me)" \
  -H "Content-Type: application/x-www-form-urlencoded" -X POST -d \
  "grant_type=authorization_code" -d "client_id=$CLIENT_ID" -d \
  "client_secret=$CLIENT_SECRET" -d "code=$CODE" \
  'https://hh.ru/oauth/token'

