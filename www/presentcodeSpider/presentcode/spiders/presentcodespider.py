import scrapy
import re
import logging
from presentcode.items import PresentCodeItem


class PresentCodeSpider(scrapy.Spider):

    name = "presentcodespider"

    start_urls = [
        "http://blackdesert.pmang.jp/notices",
        "http://blackdesert.pmang.jp/notices?page=2"
    ]
    # start_urls = ("http://blackdesert.pmang.jp/notices?page=" + str(i) for i in range(2, 10))

    def __init__(self):
        self.timeregex = re.compile(r"\d+/\d+/\d+|\d+/\d+")
        self.coderegex = re.compile(r"\w{4}\s-\s\w{4}\s-\s\w{4}")

    def parse(self, response):
        for notice_url in response.xpath("//td[@class='title']/a/@href"):

            notice_url = "http://blackdesert.pmang.jp/notices/" + notice_url.extract().split('/')[-1]

            new_request = scrapy.Request(notice_url, callback=self.parse_notice_page)
            yield new_request

    def parse_notice_page(self, response):
        for el in response.xpath("//font[@size='5']/strong"):
            presentcode_candi = el.xpath("text()").re(self.coderegex)
            if presentcode_candi:
                presentcode = presentcode_candi[0]
                url = response.url

                time = el.xpath("ancestor::div[@class='in']/p/font[@color='red']")
                if time.re(self.timeregex):
                    time = time.xpath("text()").extract()
                else:
                    logging.debug("红字没找到")
                    time = response.xpath("//div[@id='deco']//p[@class='mar_w30']/b/text() | //p[@class='mar_w30']/text() | //p[@class='mar_w30']/b/font/text()").extract()

                if len(time) > 1:
                    time = ''.join(time)
                elif len(time) == 1:
                    time = time[0]
                else:
                    logging.warning("没找到截至日期,{0}".format(url))

                yield PresentCodeItem(presentcode=presentcode, timestr=time, url=url)
        # print(self.crawler.stats.get_stats()["downloader/response_count"])
