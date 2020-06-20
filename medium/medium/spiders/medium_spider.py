# -*- coding: utf-8 -*-
import scrapy
from medium.items import ArticlesItem
from medium.utils.common import date_convert, claps_convert
from selenium import webdriver
import time
from scrapy import signals


class MediumSpider(scrapy.Spider):
    name = 'medium_spider'
    allowed_domains = ['medium.com']

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="C:/WY/tmp/chromedriver.exe") # my driver location
        self.paths = []
        super(MediumSpider, self).__init__()

    def start_requests(self):
        self.browser.get('https://medium.com/topic/popular')
        for i in range(10):
            time.sleep(3)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var "
                                        "PageLen=document.body.scrollHeight; return PageLen;")
        nodes = self.browser.find_elements_by_xpath("//section[contains(@class, 'n')]//h3[contains(@class, 'ap')]/a[1]")
        for node in nodes:
            path = node.get_attribute('href')
            self.paths.append(path)
        for path in self.paths:
            self.browser.delete_all_cookies()
            yield scrapy.Request(path, callback=self.parse, encoding="utf-8")

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MediumSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print("Medium spider closed")
        self.browser.quit()

    def parse(self, response):
        item = ArticlesItem()

        item["url"] = response.url
        item["title"] = response.xpath('//div/div/article/div/section[1]/div/div/div[1]/h1/text()').get()
        date_string = response.xpath('//section//div/div/div/div/div[1]/div[2]/span/span/div/a/text()').get()
        item["date"] = date_convert(date_string)
        item["content"] = '. '.join(response.xpath('//article/div/section/div/div/p/text()').getall())
        footer_node = response.xpath('//*[@id="root"]/div/div[position() = last()-1]/div/div[1]/div')
        item["tags"] = footer_node.xpath('//ul/li/a/text()').getall()
        item["claps"] = claps_convert(footer_node.xpath('//h4/button/text()').extract_first().rstrip())
        copyright_node = footer_node.xpath('//div/div/h2/a/text()').getall()
        item["author"] = copyright_node[0]
        item["publication"] = copyright_node[1]

        yield item
