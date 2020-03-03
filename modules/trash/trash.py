#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threadpool
import requests
import logging
import random
import os

class Trash(object):
    def __init__(self, host, uris, uaFile="user_agent.list",payloadFile="payload.list"):
        self._urlPool = []
        for uri in uris:
            url = "http://%s%s" % (host, uri)
            self._urlPool.append(url)
        uaPath = os.path.join(os.path.split(os.path.realpath(__file__))[0],"user_agent.list")
        payloadPath = os.path.join(os.path.split(os.path.realpath(__file__))[0],"payload.list")
        self._uaPool = self._read(uaPath)
        self._payloadPool = self._read(payloadPath)
    
    def _read(self, path):
        result = []
        if os.access(path, os.R_OK):
            try:
                file = open(path, 'r')
                line = file.readline().strip('\n').strip('\r')
                while line:
                    result.append(line)
                    line = file.readline().strip('\n').strip('\r')
                file.close()
                return result
            except:
                logging.warn('Loading file: ' + path + ' failed')
        else:
            logging.warn('File ' + path + ' is not readable')

    def get(self, url, ua, payload):
        target = url + "?" + payload
        headers = {
            "User-Agent": ua
        }
        try:
            requests.get(url=target, headers=headers, timeout=0.1)
        except:
            pass
    
    def post(self, url, ua, payloads):
        headers = {
            "User-Agnet": ua
        }
        data = {}
        for payload in payloads:
            temp = payload.split('=>')
            data[temp[0]] = temp[1]
        try:
            requests.post(url=url, headers=headers, data=data, timeout=0.1)
        except:
            pass

    def upload(self, url, ua, num):
        headers = {
            "User-Agent": ua
        }
        file = os.path.join(os.path.split(os.path.realpath(__file__))[0],'file', str(num) + '.php')
        with open(file,'rb') as f1:
            files = {'file':('photo.php',f1)}
        try:
            requests.post(url=url,headers=headers,timeout=0.1,files=files)
        except:
            pass

    def randSend(self):
        url = random.choice(self._urlPool)
        ua = random.choice(self._uaPool)
        method = random.choice(['get','post','upload'])
        if 'get' == method:
            payload = random.choice(self._payloadPool)
            self.get(url=url,ua=ua,payload=payload)
        elif 'post' == method:
            paramNum = random.randint(1,6)
            payloads = []
            for i in range(paramNum):
                payloads.append(random.choice(self._payloadPool))
            self.post(url=url,ua=ua,payloads=payloads)
        else:
            num = random.randint(1,14)
            self.upload(url=url,ua=ua,num=num)
            
    def start(self):
        min = random.randint(100,200)
        max = min + random.randint(200,300)
        for i in range(min, max):
            self.randSend()

if __name__ == '__main__':
    uris = ['/test1/index.php','/test1/hint.php']
    t = Trash(host='120.24.86.145:8006',uris=uris)
    t.start()
        
