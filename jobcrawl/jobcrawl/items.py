# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobcrawlItem(scrapy.Item):
    '''
    爬取的招聘信息的item,对应于每一个实体
    '''
    
    # 每个招聘的标题
    job_title = scrapy.Field()
    
    # 每个招聘的连接
    job_link = scrapy.Field()
    
    # 每个招聘的详细信息
    eachjob_company_detail = scrapy.Field()
    
    # 每个招聘的福利待遇
    eachjob_welfare = scrapy.Field()
    
    # 每个招聘的具体信息
    eachjob_company_info = scrapy.Field()


