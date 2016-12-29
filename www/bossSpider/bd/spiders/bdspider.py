import scrapy
# import logging
from bd.items import BdItem


class BdItemSpider(scrapy.Spider):

    name = "bdspider"

    start_urls = [
        "http://6214.teacup.com/blackdesertboss/bbs"
    ]

    def parse(self, response):

        # <div class="col-lg-10 col-lg-offset-1">
        transtab = str.maketrans("１２３４５６７８９０：", "1234567890:")
        for post in response.xpath("//div[@class='col-lg-10 col-lg-offset-1']")[2:13]:
            item = BdItem()
            item["title"] = post.xpath(".//a/text()").extract()[0].replace("\u3000", " ").translate(transtab)
            item["content"] = ''.join(post.xpath(".//p/text()").extract()).replace("\u3000", " ").translate(transtab)
            item["create_time"] = post.xpath(".//span[@class='pull-right']/text()").extract()[0][5:].split("(")[0]
            yield item

        # item['iconurl'] = table.xpath("//img[@alt='icon']/@src")
        # item['name'] = table.xpath("//"
