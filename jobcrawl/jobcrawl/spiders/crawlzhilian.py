# -*- coding: utf-8 -*-
import scrapy
from jobcrawl.items import JobcrawlItem


class CrawlzhilianSpider(scrapy.Spider):
    name = 'crawlzhilian'
    allowed_domains = ['sou.zhaopin.com/']
    flag = True
    # 设置爬取的起始页        
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?'         
    data = [
            # 默认-1代表所有
            # 需要查询的地区
            "jl=上海&",
            # 查询的关键字
            "kw=python&",
            "isadv=0&",
            # 是否进行筛选
            "isfilter=1&",
            # 工作经验1-3年
            "we=0103&",
            # 发布时间 1近一天 3近三天
            "pd=3&",
            #
            "sf=-1&",
            # 薪资范围,取最大值
            "st=10000&",
            # 企业性质,1 国企
            "ct=-1&",
            # 学历限制,-2代表所有 -1不限制学历,4本科及以上
            "el=-2&",
            # 工作类型 2代表全职
            "et=-1&p="
        ]
    # 页码
    page = 1
    # uuid标识符,翻页时使用,也可以不使用
    # sg=3adf9295497c41c084bbac500e661b45&

    #拼接爬取的地址                             
    start_urls = [url + "".join(data) + str(page)]
       
    def parse(self, response):
        '''           
        爬取起始页的函数                           
        '''                                       
        items = []                                
        # 获取招聘信息的标题集合                  
        job_titles = response.xpath("//div[@class='newlist_list_content']//div/a[@target='_blank']/text()[1]").extract()
        # 获取招聘信息的连接地址集合        
        job_links = response.xpath("//div[@class='newlist_list_content']//div/a[@target='_blank']/@href").extract()
        
        if len(job_titles) != 0:                   
            for i in range(0, len(job_titles)):
                item = JobcrawlItem()              
                item['job_title'] = job_titles[i].strip()+' ` '
                item['job_link'] = job_links[i]
                # 在内循环中判断每个招聘信息标题与连接是否存在
                if job_titles[i].strip() == "" or job_links[i] == "":
                    # 设置标识并跳出循环           
                    self.flag = False        
                    break                     
                items.append(item)                 
            # 遍历有具体信息的招聘信息,并向下继续爬取具体信息

            for each in items:
                yield scrapy.Request(url=each['job_link'], meta={'meta': each}, callback=self.parse_each_job, dont_filter=True)
        else:
            self.flag = False  

        if self.flag :
            self.page += 1
            yield scrapy.Request(url = self.url + "".join(self.data) + str(self.page) , callback = self.parse, dont_filter=True)


    def parse_each_job(self, response):   
        item = response.meta['meta']

        eachjob_company_detail = response.xpath("//div[@class='company-box']//li/strong/text()").extract()
 
        eachjob_welfare = response.xpath("//div[contains(@class,'terminalpage')]//div[@class='terminalpage-left']//li[1]/strong/text()").extract()[0]
        
        eachjob_company_info = ''
        eachjob_company_info_list = response.xpath("//div[contains(@class,'terminalpage')]//div[@class='tab-inner-cont']/p/text()").extract() 

        for info_each in eachjob_company_info_list:
            eachjob_company_info += info_each.strip()

        # 封装具体的详细数据
        item['eachjob_company_detail'] = eachjob_company_detail[0].strip()+eachjob_company_detail[1].strip()+' ` '
        item['eachjob_welfare'] = eachjob_welfare.strip()+' ` '
        item['eachjob_company_info'] = eachjob_company_info.strip()+' ` '
        
        # 将封装好的数据传递给管道文件处理
        yield item


