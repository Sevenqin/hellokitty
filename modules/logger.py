# -*- coding: utf-8 -*-
import sys
import threading

LogColor = {
    'info':'\033[94m',
    'success':'\033[97m',
    'warning':'\033[93m',
    'fail':'\033[91m',
    'end':'\033[0m'
}


def logger(level='info', msg=''):
    if isinstance(msg, list):
        msg = '\t'.join(msg)
    elif isinstance(msg, dict):
        msg = [k+':'+v for k, v in msg.items()]
        msg = '\t'.join(msg)

    if level not in LogColor.keys():
        level = 'end'
    if level == 'success':
        msg = '[+]'+msg
    elif level == 'warning':
        msg = '[!]'+msg
    elif level == 'fail':
        msg = '[-]'+msg
    threadLock = threading.Lock()
    threadLock.acquire()
    if not sys.platform.startswith('win'):
        print('{}{}{}'.format(LogColor[level],msg,LogColor['end']))
    else:
        print(msg)
    threadLock.release()

    
