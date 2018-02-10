
# redis 数据库地址
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
PASSWORD = None
REDIS_KEY = 'proxy'

# ip存在状态分数
PROXY_SCORE_MAX = 100
PROXY_SCORE_MIN = 0

# 初始分数
PROXY_SATUS_INIT = 20

# ip池最大数目
IP_MAX_COUNT = 500

# 测试周期和抓取周期
CHECK_CYCLE = 20
# 最大测试量
TEST_COUNT_ = 20


# 你要抓取的网站
CHECK_URL = 'http://www.baidu.com'


# 开关
TESTER = True
GETTER = True
API = True


# 设置提取api
API_HOST = '127.0.0.1'
API_PORT = 5555
