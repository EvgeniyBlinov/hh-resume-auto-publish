import os
import sys
import time
import requests
import logging
import json


class HH(object):

    """Docstring for HH. """

    def __init__(self, s: requests.sessions.Session, client_id: str, client_secret: str, code: str, api_token: str, ref_token: str, resume_id: str):
        """TODO: to be defined. """
        self.s = s
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.api_token = api_token
        self.ref_token = ref_token

        s.headers.update({'Authorization': f'Bearer {self.api_token}'})

        if resume_id:
            self.resume_id = resume_id
        else:
            self.resume_id = self.get_resume_list()


    def get_resume_list(self):
        url = 'https://api.hh.ru/resumes/mine'
        r = self.s.get(url)

        if r.status_code == 200:
            data = r.json()
            resume_ids = [resume['id'] for resume in data['items']]
            log.info('Loaded resume list ({0} items)'. format(len(resume_ids)))
            return resume_ids
        else:
            msg = "Can't get resume list from hh.ru!"
            log.error(msg)
            exit()



    def update_resume(self):
        resume_id = self.resume_id
        url = f'https://api.hh.ru/resumes/{resume_id}/publish'
        s.headers.update({'Authorization': f'Bearer {self.api_token}'})
        r = s.post(url)

        if r.status_code == 204:
            log.info(f'update_resume {resume_id}: updated')
        elif r.status_code == 429:
            log.info(f'update_resume {resume_id}: too many requests')
        elif r.status_code == 400:
            log.info(f'update_resume {resume_id}: can\'t update because resume is incorrect')
        elif r.status_code == 403:
            data = r.json()
            log.error(f'update_resume {resume_id}: auth required: %s' % data)
            oauth_bad_authorization = {'value': 'bad_authorization', 'type': 'oauth'}
            if 'errors' in data and oauth_bad_authorization in data['errors']:
                self.update_authorization_code()
        else:
            log.error(f'update_resume {resume_id}: unknown status: %s' % r.json())


    def update_token(self):
        url='https://hh.ru/oauth/token'
        data={'grant_type': 'refresh_token',
            'refresh_token': self.ref_token}

        r=requests.post(url = url, data = data)

        if r.status_code == 200:
            tokens=r.json()
            self.api_token=tokens['access_token']
            self.ref_token=tokens['refresh_token']
            log.info('update_token: token updated')
            s.headers.update({'Authorization': f'Bearer {self.api_token}'})
        elif r.status_code == 400:
            data = r.json()
            log.info('update_token: token not expired: %s' % data)


    def update_authorization_code(self):
        url='https://hh.ru/oauth/token'
        data={'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.code}

        r=requests.post(url = url, data = data)


        if r.status_code == 200:
            tokens=r.json()
            self.api_token=tokens['access_token']
            self.ref_token=tokens['refresh_token']
            log.info('token updated')
            s.headers.update({'Authorization': f'Bearer {self.api_token}'})
        elif r.status_code == 400:
            log.info('token not expired')
            # log.error('update_authorization_code: %s' % r.json())


    def update(self):
        while True:
            # check updatability token before request to API
            self.update_token()

            for id in self.resume_id:
                self.update_resume()
                time.sleep(5)

            # sleep 60 minutes
            log.info('going sleep...')
            time.sleep(60 * 60)



# check if hh.ru API tokens is in environment variables
if 'HH_TOKEN' in os.environ and 'HH_REFRESH_TOKEN' in os.environ:
    api_token = os.environ['HH_TOKEN']
    ref_token = os.environ['HH_REFRESH_TOKEN']
else:
    sys.exit("hh.ru API token is not specified! "
             "Go to read README.md",)

# if 'CLIENT_ID' in os.environ and 'CLIENT_SECRET' in os.environ and 'CODE' in os.environ:
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
code = os.environ['CODE']
resume_id = os.getenv('HH_RESUME_ID', '') 

log = logging.getLogger('hh-resume-auto-publish')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

s = requests.Session()

hh = HH(s, client_id, client_secret, code, api_token, ref_token, resume_id)


# main loop
if __name__ == '__main__':
    hh.update()
