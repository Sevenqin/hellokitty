# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from modules.execute import execute_command,ExecuteFailException
from utils import Utils
from configuration import configuration

class Runner:
    def __init__(self,webshell):
        self.host = webshell.host
        self.locations = webshell.locations
        self.password = webshell.password

    def execute(self,cmd):
        for location in self.locations:
            url = 'http://{}{}'.format(self.host,location)
            try:
                return execute_command(url,self.password,cmd,configuration.phpFunction)
            except ExecuteFailException:
                continue
        return None