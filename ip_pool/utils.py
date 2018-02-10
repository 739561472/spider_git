import requests

_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
}


def get_page(url, kwargs=dict):
    if isinstance(kwargs, dict):
        headers = dict(_headers, **kwargs)
    else:
        headers = _headers
    try:
        respones = requests.get(url=url, headers=headers)
        if respones.status_code == 200:
            return respones.text
        else:
            print('状态码错误')
    except requests.ConnectionError as e:
        print('连接错误', e)

