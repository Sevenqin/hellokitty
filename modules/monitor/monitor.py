#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import threadpool
from threading import Lock
from functools import partial
import sys
sys.path.append('../..')
from utils import Utils
from configuration import configuration


class SMonitor:
    def __init__(self, host, shellLocations, password=None):
        self.host = host
        self.shellLocations = shellLocations
        self.password = password if password else Utils.getPassword(host)

    def scan(self):
        shell = []
        for shellLocation in self.shellLocations:
            url = 'http://{}{}'.format(self.host, shellLocation)
            try:
                resp = requests.post(url, headers=configuration.headers, data={
                    self.password: 'echo seven;'
                }, timeout=2)
                if 'seven' in resp.text:
                    shell.append(url)
            except:
                continue
        return shell


class Monitor(object):

    # conf - configuration
    def __init__(self, conf):
        self._pool = conf.pool
        self._headers = conf.headers
        self._targets = conf.targets
        self._shells = conf.shellLocations
        self._result = {}

    def check(self, url, host):
        try:
            password = Utils.getPassword(host)
            resp = requests.post(url=url, headers=self._headers,data={
                password:'echo seven;'
            },timeout=3)
            if 'seven' in resp.text:
                return True
            else:
                return False
        except:
            return False

    def checkHost(self, host, shells):
        result = {}
        count = 0
        result['shell'] = []
        for shell in shells:
            url = "http://%s%s" % (host, shell)
            if self.check(url=url,host=host):
                count = count + 1
                result['shell'].append(url)
        result['count'] = count
        return result

    def scanCallback(self, request, result):
        target = request.args[0]
        self._result[target] = result

    def scan(self):
        params = []
        self._result = {}
        for target in self._targets:
            param = [target, self._shells]
            params.append((param, None))
        reqs = threadpool.makeRequests(
            self.checkHost, params, self.scanCallback)
        [self._pool.putRequest(req) for req in reqs]
        self._pool.wait()
        return self._result


if __name__ == '__main__':
    import sys
    import json
    sys.path.append('../..')
    from configuration import configuration
    m = Monitor(configuration)
    print(json.dumps(m.scan()))
