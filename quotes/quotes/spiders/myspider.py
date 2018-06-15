# -*- coding: utf-8 -*-
import scrapy
from quotes.items import QuotesItem


class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    page = 0

    def parse(self, response):
        item = QuotesItem()
        for quote in response.css('div.quote'):
            item['quotes'] = quote.css('span.text::text').extract_first().replace("'", "\\'")
            item['author'] = quote.css('small.author::text').extract_first()
            link = quote.css('a::attr(href)').extract_first()
            item['author_link'] = response.urljoin(link)
            item['tags'] = ';'.join(quote.css('div.tags a.tag::text').extract())
            yield item

        self.page += 1
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page and self.page < 3:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
