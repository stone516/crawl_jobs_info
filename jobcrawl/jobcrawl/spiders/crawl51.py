# -*- coding: utf-8 -*-
import scrapy 
from jobcrawl.items import JobcrawlItem


class Crawl51Spider(scrapy.Spider):
    '''
    设置爬取51job的爬虫
    '''
    name = 'crawl51'
    allowed_domains = ['www.51job.com']
                              
    # 设置爬取的起始页        
    url = 'http://search.51job.com/list/'         
                         
    # 爬取的区域以及其他信息  020000 上海         
    search_region = '020000'+',000000,0000,00,'    
                                                   
    # 发布时间 0: 24小时内  1:三天内 2 :近一周 3:近一月 4:其他 9 所有
    publishdate = '1,'                            
                                                   
    # 薪资范围 06: 8-10, 07:10-15, 08:15-20 ,09: 20-20,...99:所有,单位k
    salary_range = '07,'                          
                                                
    # 需要爬取的关键字                             
    keyword = "python"+',2,'                         

    # 翻页停止的条件                               
    flag = True                                   
                                         
    # 爬取的起始页                   
    page = 1                         
                       
    end = ".html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    # 拼接爬取的地址                             
    start_urls = [url + search_region + publishdate + salary_range + keyword + str(page) + end]
       
    def parse(self, response):
        '''           
        爬取起始页的函数                           
        '''                                       
        items = []                                
        # 获取招聘信息的标题集合                  
        job_titles = response.xpath("//div[@class='el']/p/span/a[@title]/text()").extract()
        # 获取招聘信息的连接地址集合        
        job_links = response.xpath("//div[@class='el']/p/span/a/@href").extract()
        
        if len(job_titles) != 0:                   
            for i in range(0, len(job_titles)):
                item = JobcrawlItem()              
                item['job_title'] = job_titles[i].strip()+' ` '
                item['job_link'] = job_links[i]
                # 在内循环中判断每个招聘信息标题与连接是否存在
                if job_titles[i] == "" or job_links[i] == "":
                    # 设置标识并跳出循环           
                    self.flag = False             
                    continue                    
                items.append(item)                 
            # 遍历有具体信息的招聘信息,并向下继续爬取具体信息

            for each in items:
                yield scrapy.Request(url=each['job_link'], meta={'meta': each}, callback=self.parse_each_job, dont_filter=True)
        else:
            self.flag = False  

        if self.flag :
            self.page += 1
            yield scrapy.Request(url = self.url + self.search_region + self.publishdate + self.salary_range + self.keyword + str(self.page) + self.end, callback = self.parse, dont_filter=True)


    def parse_each_job(self, response):   
        item = response.meta['meta']

        eachjob_company_detail = response.xpath("//div[contains(@class,'tCompanyPage')]//div[@class='cn']/p[2]/text()").extract()[0]
 
        eachjob_welfare = response.xpath("//div[contains(@class,'tCompanyPage')]//div[@class='cn']/strong/text()").extract()[0]
        eachjob_company_info = ''
        eachjob_company_info_list = response.xpath("//div[contains(@class,'tCompanyPage')]//div[contains(@class,'bmsg')]/text()").extract()
        
        for info_each in eachjob_company_info_list:
            eachjob_company_info += info_each.strip()

        # 封装具体的详细数据
        item['eachjob_company_detail'] = eachjob_company_detail.strip()+' ` '
        item['eachjob_welfare'] = eachjob_welfare.strip()+' ` '
        item['eachjob_company_info'] = eachjob_company_info.strip()+' ` '
        
        # 将封装好的数据传递给管道文件处理
        yield item


