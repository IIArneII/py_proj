import requests
from consts import api_root
import datetime
import json as j

try:
    resp = requests.get(f'{api_root}/posts/', params={'for_user_id': 5}).json()
    # resp = requests.put(f'{api_root}/posts/al/like/1').json()
    # resp = requests.get(f'{api_root}/posts').json()

    print(j.dumps(resp, indent=4))
except Exception as e:
    print(e)
