# -*- coding: utf-8 -*-
import sys
import base64
sys.path.append('..')
from utils import Utils
from models.engine import Engine
from configuration import configuration

class Horse:
    def __init__(self,host):
        self.host = host
        self.conf = configuration
        self.password = Utils.getPassword(host)
        self.default = self.generate(configuration.defaultHorse)
        self.simple = self.generate('simple.php')

    def generate(self, kind):
        return Engine(kind).apply({'password': self.password})


if __name__ == '__main__':
    print(Horse('192.168.1.1').default)
