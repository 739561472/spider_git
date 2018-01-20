# coding:utf-8
import uuid
from PIL import Image

import requests

client = requests.Session()
# 人眼识别大法！！！


def get_qr_code(codetoken):
    # 使用uuid下载验证码图片
    qr_code = client.get('http://hz.fangjia.com/randomCode?type=validate&codeToeken=' + codetoken + '&time=3809')
    open('captcha.jpg', 'wb').write(qr_code.content)
    # 打开并显示图片
    img = Image.open('captcha.jpg')
    img.show()


def handler_captcha():
    codetoken = str(uuid.uuid4())      # 自行生成uuid
    get_qr_code(codetoken)
    #  人眼识别并输入验证码-_-||
    code = input("请输入验证码: \n")
    result = client.get('http://hz.fangjia.com/checkCode?code=' + code + '&guid=' + codetoken).json()
    return result['msg']


# a = handler_captcha()
# print(a)

