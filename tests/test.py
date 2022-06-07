import requests
from consts import api_root
import datetime
import json as j

try:
    resp = requests.post(f'{api_root}/posts')
    print(resp)
    print(resp.json())
except Exception as e:
    print(e)
