# encoding: utf-8
from lxml import etree
from bs4 import BeautifulSoup


class Soup(object):
    def __init__(self, response):
        self.soup = BeautifulSoup(response, 'lxml')

    def find_all(self, reg):
        try:
            res = self.soup.find_all(reg)
            return res
        except AttributeError as e:
            print(e, '没有找到相应标签')
            return None

    def find(self, reg):
        try:
            res = self.soup.find(reg)
            return res
        except AttributeError as e:
            print(e, '没有找到相应标签')
            return None













