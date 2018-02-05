import random
import requests
from captcha import get_captcha
from lxml import etree
from config import *
from JSEncrypt import JSEncrypt

session = requests.session()


def login():
    url = 'https://passport.jd.com/uc/login?ltype=logout'
    l_headers = {
        'Referer': 'https://www.jd.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    res = session.get(url, headers=l_headers).text
    selectors = etree.HTML(res)
    sa_token = selectors.xpath('//input[@id="sa_token"]/@value')[0]
    uuid = selectors.xpath('//input[@id="uuid"]/@value')[0]
    # authcode = selectors.xpath('//img[@class="verify-code"/@src2]')[0]
    login_url = 'https://passport.jd.com/uc/loginService?uuid={uuid}&ltype=logout&r={random}&version=2015'\
                .format(uuid=uuid, random=random.random())
    form_data = {
        'uuid': uuid,
        'eid': EID,
        'fp': FP,
        '_t': '_t',
        'loginType': 'f',
        'loginname': '',
        'nloginpwd': JSEncrypt(input('请输入您的密码！')),
        'chkRememberMe': '',
        'authcode': get_captcha(uuid),
        'pubKey': PUBKEY,
        'sa_token': sa_token,
    }
    # if authcode:
    #   form_data['authcode'] = get_captcha(uuid)
    res = session.post(url=login_url, data=form_data, headers=l_headers).text
    print(res)


def main():
    login()


if __name__ == '__main__':
    main()
