# hh-resume-auto-publish
Script to update your resumes (CV) on hh.ru automatically.

## How to use
1. Get tokens:
  * Go to `https://dev.hh.ru/admin` and register app for get <client_id> and <client_secret>
  * Go to `https://hh.ru/oauth/authorize?response_type=code&client_id=<client_id>` for get `https://hh.ru/?code=<code>`
  * Put them all to `get_user_tokens.sh`
2. Paste tokens to `docker-compose.yml` file on line 9 and 10
3. `docker-compose up -d`
