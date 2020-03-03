#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import logging
import re
import base64
import psutil
from uuid import uuid1

from configuration import configuration as config

class Utils:
    @staticmethod
    def md5(src):
        return hashlib.md5(src.encode("utf-8")).hexdigest()

    @staticmethod
    def base64(src):
        return base64.b64encode(src.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base64_d(src):
        return base64.b64decode(src.encode('utf-8')).decode('utf-8')

    @classmethod
    def getPassword(cls, host):
        salt = config.salt
        return cls.md5(host+salt)

    @classmethod
    def getShellPath(cls,host):
        return [host+path for path in config.shellLocations]
        
    @classmethod
    def getHostList(cls):
        return config.targets

    @staticmethod
    def parseUrl(url):
        result = {}
        pattern = r"(http|https|ftp)://([a-z0-9A-Z\-_\.]+)(:(\d+)){0,1}(/{1,}[a-z0-9A-Z\-_\.]+){0,1}"
        search = re.search(pattern,url)
        if search is None:
            logging.warn('Url format error.')
            return None
        else:
            result['protocol'] = search.group(1)
            result['host'] = search.group(2)
            port = search.group(4)
            if port:
                result['port'] = int(search.group(4))
            else:
                result['port']= 80
            result['uri'] = search.group(5)
        return result
    
    @staticmethod
    def assembleUrl(host, uri, port=80, protocol='http'):
        if (port == 80 and protocol == 'http') or (port == 443 and protocol == 'https') or (port == 21 and protocol == 'ftp'):
            return protocol + "://" + host + uri
        else:
            return protocol + "://" + host + ":" + str(port) + uri
    
    @staticmethod
    def getLocalAddress():
        netcard_info = []
        info = psutil.net_if_addrs()
        for k,v in info.items():
            for item in v:
                if item[0] == 2 and not item[1] == '127.0.0.1':
                    netcard_info.append((k.decode('gbk'), item[1]))
        return netcard_info
    
    @staticmethod
    def randmd5():
        return hashlib.md5(str(uuid1()).encode("utf-8")).hexdigest()

if __name__ == '__main__':
    import json
    print(Utils.randmd5())
