# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse


class SeleniumMiddleware(object):

    def process_request(self, request, spider):

        spider.browser.get(request.url)

        return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                            request=request, encoding="utf-8")
