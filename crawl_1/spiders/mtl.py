# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MtlSpider(CrawlSpider):
    name = 'mtl'
    allowed_domains = ['meitulu.com']
    start_urls = ['http://meitulu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.meitulu.com/t/.*?/', restrict_xpaths="//ul[@id='tag_ul']/li"), callback='parse_item'),
    )

    def parse_item(self, response):
        # 获取所有的图集
        links = response.xpath("//ul[@class='img']/li")
        for i in links:
            item = {}
            item["title"] = response.xpath("//title/text()").extract_first().split("_")[0]
            item["name"] = i.xpath(".//p[@class='p_title']/a/text()").extract_first()
            next_url = i.xpath("./a/@href").extract_first()
            yield scrapy.Request(
                next_url,
                callback=self.parse_dual,
                meta={"item": item}
            )
        try:
            next_page_url = response.xpath("//div[@id='pages']/a")
            if len(next_page_url) > 0:
                next_page_url = next_page_url[-1]
            next_page_url = next_page_url.xpath("./@href").extract_first()
            if next_page_url is not None:
                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse_item,
                )
        except:
            pass

    def parse_dual(self, response):
        item = response.meta["item"]
        image_list = response.xpath("//div[@class='content']/center/img")
        for i in image_list:
            item["image_name"] = i.xpath("./@alt").extract_first()
            item["image"] = i.xpath("./@src").extract_first()
            yield item
        next_page_url = response.xpath("//div[@id='pages']/a")
        if len(next_page_url) > 0:
            next_page_url = next_page_url[-1]
        next_page_url = next_page_url.xpath("./@href").extract_first()
        print(next_page_url)
        if next_page_url is not None:
            yield scrapy.Request(
                "https://www.meitulu.com" + next_page_url,
                callback=self.parse_dual,
                meta={"item": item}
            )