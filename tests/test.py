import requests
from consts import api_root
import datetime
import json as j

try:
    # resp = requests.post(f'{api_root}/users', json={
    #     'login': 'al4',
    #     'password': '123',
    #     'email': 'al@aa3l',
    #     'birthday': '2020-12-12',
    #     'last_name': 'ss',
    #     'first_name': 'ss',
    # }).json()
    resp = requests.get(f'{api_root}/users/al').json()
    print(j.dumps(resp, indent=4))
except Exception as e:
    print(e)
