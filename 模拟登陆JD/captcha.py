import time
import requests
from PIL import Image


session = requests.session()


def get_captcha(uuid):
    t = time.time()
    yys = int(round(t * 1000))
    headers = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Host': 'authcode.jd.com',
        'Pragma': 'no-cache',
        'Referer': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    url = 'https://authcode.jd.com/verify/image?a=1&acid={}&uid={}&yys={}'.format(uuid, uuid, yys)
    img = session.get(url=url, headers=headers).content
    open('captcha.jpg', 'wb').write(img)
    img = Image.open('captcha.jpg')
    img.show()
    authcode = input('请输入验证码：')
    return authcode
