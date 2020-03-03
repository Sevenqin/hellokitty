#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import logging

approot = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..')

class Engine(object):
    def __init__(self, template):
        self._path = os.path.join(approot, "templates", template+".temp")
        if os.access(self._path, os.R_OK):
            try:
                with open(self._path, 'r') as temp:
                    self._template = temp.read()
            except:
                logging.warn('Reading template ' + self._path + ' failed')
        else:
            logging.warn('Loading template ' + self._path + ' failed')
    
    def apply(self, dic):
        return self._template % dic

    def base64(self, dic):
        return base64.b64encode(self.apply(dic).encode('utf-8')).decode('utf-8')
        

if __name__ == '__main__':
    php = Engine('zoo.php')
    print(php.base64({"password":"123456"}))
