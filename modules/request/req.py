#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../..')
from configuration import configuration as config
import requests

def get(url, cookies=None, params=None, headers=config.headers, timeout=config.timeout, verify=False):
    return requests.get(url=url, cookies=cookies, params=params, headers=headers, timeout=timeout, verify=verify)

def post(url, cookies=None, params=None, data=None, files=None, headers=config.headers, timeout=config.timeout, verify=False):
    return requests.post(url=url, cookies=cookies, params=params, data=data, files=files, headers=headers, timeout=timeout, verify=verify)

class Session(requests.Session):
    def request(self, method, url,
            params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None):
        if not timeout:
            timeout = config.timeout
        return super().request(method, url,
            params, data, headers, cookies, files,
            auth, timeout, allow_redirects, proxies,
            hooks, stream, verify, cert, json)

if __name__ == '__main__':
    resp = post(url="http://www.baidu.com")
    print(resp.headers)
