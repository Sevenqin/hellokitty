#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import base64

from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5 as pkcs1

class RSATool(object):
    def __init__(self, pubFile='public.pem', priFile='private.pem'):
        base = os.path.split(os.path.realpath(__file__))[0]
        try:
            with open(os.path.join(base,pubFile),'r') as pub:
                self.pubKey = pkcs1.new(rsa.importKey(pub.read()))
            with open(os.path.join(base,priFile),'r') as pri:
                self.priKey = pkcs1.new(rsa.importKey(pri.read()))
        except:
            logging.error('Load RSA key-pair failed: ' + base)
        
    def encrypt(self, plain):
        res = []
        for i in range(0, len(plain), 200):
            res.append(self.pubKey.encrypt(plain[i:i+200]))
        return base64.b64encode("".join(res))
    
    def decrypt(self, cipher):
        res = []
        c = base64.b64decode(cipher)
        for i in range(0, len(c), 256):
            res.append(self.priKey.decrypt(c[i:i+256], None))
        return "".join(res)

rsatool = RSATool()
