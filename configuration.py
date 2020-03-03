#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
import requests
import threadpool

# from modules.encrypt.rsatool import rsatool
from modules.sitemap.mapper import loadmap

class Configuration(object):
    #path: the location of the config file
    def __init__(self, path='configuration.json'):
        self.load(path)

    # save current configuration to json file as default
    def save(self):
        tmpConfig = {}
        for k in self._config:
            tmpConfig[k] = getattr(self,k)
        if os.access(self._path, os.W_OK):
            try:
                with open(self._path, 'w') as conf:
                    conf.write(json.dumps(tmpConfig, indent=4))
                    self._config = tmpConfig
                    logging.debug('Configuration Saved')
            except:
                logging.error('Saving Configuration Failed')
        else:
            logging.error('Configuration File occupied')

    def getConfig(self):
        return self._config

    def addTarget(self, target):
        if not target in getattr(self,'targets'):
            getattr(self,'targets').append(target)
    
    def removeTarget(self, target):
        while target in getattr(self,'targets'):
            getattr(self,'targets').remove(target)

    def addShell(self, uri):
        while not uri in getattr(self,'shellLocations'):
            getattr(self,'shellLocations').append(uri)
    
    def removeShell(self, uri):
        while uri in getattr(self,'shellLocations'):
            getattr(self,'shellLocations').remove(uri)

    def load(self, path):
        self._path = os.path.join(os.path.split(os.path.realpath(__file__))[0],path)
        if os.access(self._path, os.R_OK):
            with open(self._path,'r') as conf:
                try:
                    config = json.loads(conf.read())
                    self._config = config
                    for k,v in config.items():
                        setattr(self,k,v)
                    pool = threadpool.ThreadPool(getattr(self,'poolSize',16))
                    setattr(self, 'pool', pool)
                    setattr(self, 'sitemap', loadmap())
                    logging.debug('Configuration file loaded')
                except:
                    logging.error('Configuration file format error: ' + self._path)
        else:
            logging.error('Load configuration error: ' + self._path)

    def reload(self):
        self.load(self._path)
        self.pool = threadpool.ThreadPool(getattr(self,'poolSize',16))
        self.sitemap = loadmap()



configuration = Configuration()

if __name__ == '__main__':
    print(configuration.sitemap)