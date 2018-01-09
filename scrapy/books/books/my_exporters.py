# -*- coing:utf-8 -*-

from scrapy.exporters import BaseItemExporter
import xlwt

class ExcelItemExporter(BaseItemExporter):
    def __init__(self,file,**kwargs):
        self._configure(kwargs)
        self.file = file
        self.wbook = xlwt.Workbook()
        self.wsheet = self.wbook.add_sheet('scrapybook')
        self.roe = 0
    def finish_exporter(self):
        self.wbook.save(self.file)

    def export_item(self, item):
        field = self._get_serialized_fields(item)
        for col,v in enumerate(x for _,x in field):
            self.wsheet.write(self.row,col,v)
        self.row+=10