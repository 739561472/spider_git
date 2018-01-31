
from captcha.image import ImageCaptcha  # pip install captcha
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random

# 验证码中的字符, 就不用汉字了
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
# ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
#             'V', 'W', 'X', 'Y', 'Z']
# 有大写可以加上大写字符
# + ALPHABET
# , n_len, n_class = 72, 30, 4, len(characters)


# 验证码一般都无视大小写；验证码长度4个字符
def random_captcha_text(char_set=number + alphabet, captcha_size=4):
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return captcha_text


# 生成字符对应的验证码
def gen_captcha_text_and_image():
    width, height, n_len, n_class = 144, 60, 4, 5  # len(characters)
    image = ImageCaptcha(width=width, height=height, font_sizes=(36, 43, 48))

    captcha_text = ''.join(random_captcha_text())

    captcha = image.generate(captcha_text)
    image.write(captcha_text, captcha_text + '.jpg')  # 写到文件

    captcha_image = Image.open(captcha)
    captcha_image = np.array(captcha_image)
    return captcha_text, captcha_image


if __name__ == '__main__':
    # 测试
    text, image = gen_captcha_text_and_image()
    f = plt.figure()
    ax = f.add_subplot(111)
    ax.text(0.1, 0.9, text, ha='center', va='center', transform=ax.transAxes)
    print(type(image))