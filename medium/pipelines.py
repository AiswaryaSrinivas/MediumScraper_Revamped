# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#https://stackoverflow.com/questions/32743469/scrapy-python-multiple-item-classes-in-one-pipeline

from scrapy.exporters import CsvItemExporter
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from datetime import datetime
from datetime import timedelta
import os

def item_type(item):
    return type(item).__name__.replace('Item','').lower()  # PostsItem =>Post

class MultiCSVItemPipeline(object):
    SaveTypes = ['posts','tags','collections', 'users']
    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        self.CSVDir=os.getcwd()+"//"+"data//"
        if not os.path.exists(self.CSVDir):
            os.makedirs(self.CSVDir)

    def spider_opened(self, spider):
        self.files = dict([ (name, open(self.CSVDir+name+"_"+datetime.now().strftime("%Y%m%d")+'.csv','a')) for name in self.SaveTypes ])
        self.exporter = dict([ (name,CsvItemExporter(self.files[name])) for name in self.SaveTypes])
        
        [e.start_exporting() for e in self.exporter.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporter.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = item_type(item)
        #print(what)
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item
