# hh-resume-auto-publish
Script to update your resumes (CV) on hh.ru automatically.

## How to use
0. Check installed packages(jq, awk, sed, docker, docker-compose)
1. Get tokens:
  * Go to `https://dev.hh.ru/admin` and register app for get <client_id> and <client_secret>
  `set -o allexport; source .env; set +o allexport;`
  * Go to `https://hh.ru/oauth/authorize?response_type=code&client_id=${CLIENT_ID}` for get `https://hh.ru/?code=<code>`
  * Put them all to `.env`
2. `docker-compose run hh-updater /usr/bin/env python updater.py code`
3. `docker-compose up -d`
