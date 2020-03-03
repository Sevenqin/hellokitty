'''
This is a default payload
if there is a backdoor in upload/upload.php,and key is pass
The real situation is much more complex
'''
import sys
import base64
sys.path.append('..')
from models.payload import Payload,PayloadFailException
import requests
from models.horse import Horse
from utils import Utils


class P(Payload):
    def attack(self):
        try:
            url = 'http://{0}/index.php'.format(self.host)
            res = requests.get(url,timeout=2)
            if res.status_code == 200:
                return url,'a'
            else:
                raise PayloadFailException
        except:
            raise PayloadFailException


