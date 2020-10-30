import os
import sys
import time
import requests
import logging
import json

log = logging.getLogger('hh-resume-auto-publish')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


def get_resume_list():
    url = 'https://api.hh.ru/resumes/mine'
    r = s.get(url)

    if r.status_code == 200:
        data = r.json()
        resume_ids = [resume['id'] for resume in data['items']]
        log.info('Loaded resume list ({0} items)'. format(len(resume_ids)))
        return resume_ids
    else:
        msg = "Can't get resume list from hh.ru!"
        log.error(msg)
        exit()


def update_resume(resume_id):
    url = f'https://api.hh.ru/resumes/{resume_id}/publish'
    r = s.post(url)

    if r.status_code == 204:
        log.info(f'{resume_id}: updated')
    elif r.status_code == 429:
        log.info(f'{resume_id}: too many requests')
    elif r.status_code == 400:
        log.info(f'{resume_id}: can\'t update because resume is incorrect')
    elif r.status_code == 403:
        log.error(f'{resume_id}: auth required')
    else:
        log.error(f'{resume_id}: unknown status')


def update_token():
    global ref_token
    global api_token
    url='https://hh.ru/oauth/token'
    data={'grant_type': 'refresh_token',
          'refresh_token': ref_token}
    r=requests.post(url = url, data = data)

    if r.status_code == 200:
        tokens=r.json()
        api_token=tokens['access_token']
        ref_token=tokens['refresh_token']
        log.info('token updated')
        s.headers.update({'Authorization': f'Bearer {api_token}'})
    elif r.status_code == 400:
        log.info('token not expired')


# check if hh.ru API tokens is in environment variables
if 'HH_TOKEN' in os.environ and 'HH_REFRESH_TOKEN' in os.environ:
    api_token = os.environ['HH_TOKEN']
    ref_token = os.environ['HH_REFRESH_TOKEN']
else:
    sys.exit("hh.ru API token is not specified! "
             "Go to read README.md",)


s = requests.Session()
s.headers.update({'Authorization': f'Bearer {api_token}'})


# check if hh.ru resume ID is in environment variables
if 'HH_RESUME_ID' in os.environ:
    # then update only that resume
    resume_id_list = [os.environ['HH_RESUME_ID']]
else:
    # else update all available resumes
    resume_id_list = get_resume_list()


# main loop
if __name__ == '__main__':
    while True:
        # check updatability token before request to API
        update_token()

        for id in resume_id_list:
            update_resume(id)
            time.sleep(5)

        # sleep 60 minutes
        log.info('going sleep...')
        time.sleep(60 * 60)
