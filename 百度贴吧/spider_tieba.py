# -*- coding: utf-8 -*-

__author__ = 'Hth'

import urllib.request
import urllib.error
import re
import os

class BDTB:
    def __init__(self, baseurl, seelz):
        self.baseurl = baseurl
        self.seelz = '?see_lz=' + str(seelz)
        self.tool = Tools()
        self.file = None
        self.default = '百度贴吧'

    def writeTitle(self,title):
        if title != None:
            self.file = open('D:/pycharm/PycharmProjects/spder_demo/output/tieba/' + title + '.txt','wb')
        else:
            print('标题获取失败,以默认标题命名')
            self.file = open('D:/pycharm/PycharmProjects/spder_demo/output/tieba/' + self.default + '.txt','wb')

    def saveFile(self,data,title):
        path = ('D:/pycharm/PycharmProjects/spder_demo/output/tieba/' + title + '.txt')
        #if os.path.exists(path):
        self.file = open(path, 'w')
        self.file.write(data)
        self.file.close()

    def get_html(self, pagenum):
        try:
            url = self.baseurl + self.seelz + '&pn=' + str(pagenum)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # data = response.read()
            # data = data.decode('utf-8')
            response = response.read().decode('utf-8')
            return response
        except urllib.error.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接百度贴吧失败,错误原因:", e.reason)
                return None

    def get_title(self):
        html = self.get_html(1)
        reg = r'<h3 class="core_title_txt pull-left text-overflow  " title=".*?" style="width: 396px">(.*?)</h3>'
        pattern = re.compile(reg, re.S)
        result = re.findall(pattern, str(html))
        # pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>', re.S)
        # result = re.search(pattern, html)
        if result:
            #print(str(result[0]))
            return str(result[0])
        else:
            return print('error')

    def get_pagenum(self):
        html = self.get_html(1)
        reg = r'<span class="red">(.*?)</span>'
        pattern = re.compile(reg, re.S)
        pagenum = re.findall(pattern, str(html))
        #print(pagenum[0])
        return pagenum[0]

    def get_context(self, html):
        reg = r'<div id="post_content_.*?">(.*?)</div>'
        pattern = re.compile(reg, re.S)
        items = re.findall(pattern, str(html))
        # print(context[0])
        contexts = []
        for item in items:
            context = self.tool.repalce(item)
            contexts.append(context)
            #print(contexts)
        return contexts
            #self.saveFile(items)



    def spder_start(self):
        pagenum = self.get_pagenum()
        title = self.get_title()
        self.writeTitle(title)
        contexts = ''
        print('正在写入文件......')
        for n in range(1,int(pagenum)+1):
            if n == None:
                print('页码错误！')
            else:
                #print(n)
                html = self.get_html(n)
                context = self.get_context(html)
                for x in context:
                    contexts = contexts + x
                    print(x)
                #for x in context:
                #    i=0
                #    contexts = contexts+context[i]
                #    i+=1
                    #print(x)
        self.saveFile(contexts,title)
        print('数据写入完成!!!!!!!!!!!')
                #contexts.append(self.get_context(html))
            #self.saveFile(item)
            #return context
            #self.saveFile(bytes(context),title)




class Tools:
    removeImg = re.compile(r'<img.*?>|/s{10}')
    removeBR = re.compile(r'<br>')
    removeA = re.compile(r'<a.*?>|</a>')

    def repalce(self, str):
        str = re.sub(self.removeImg, '', str)
        str = re.sub(self.removeBR, '', str)
        str = re.sub(self.removeA,'',str)
        return str.strip()

# 3138733512
# topic_num = input('请输入帖子编号：')
baseurl = 'https://tieba.baidu.com/p/3138733512'# +topic_num
seelz = 1  # input('是否只看楼主（是填1否填0）：')
spder = BDTB(baseurl, seelz)
spder.spder_start()


