# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jobcrawl import settings
import csv
import itertools
import time
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class JobcrawlPipeline(object):
    csvwriter = None
    c = None

    def __init__(self):
        local_time = time.strftime('%Y%m%d',time.localtime(time.time()))
        self.filename = 'job_info_' + str(local_time) + '.csv'
        self.c = open(self.filename, 'a')
        self.csvwriter = csv.writer(self.c)
        self.csvwriter.writerow(['job_title`','eachjob_welfare`','eachjob_company_detail`','eachjob_company_info`','job_link`'])

    def process_item(self, item, spider):
        str = [item['job_title'],item['eachjob_welfare'],item['eachjob_company_detail'],item['eachjob_company_info'],item['job_link']]
        
        self.csvwriter.writerow(str)

        return item

    def spider_close(self):
        self.c.close()


