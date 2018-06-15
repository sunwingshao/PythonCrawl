# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class QuotesPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.db = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("HOST"),
            database=crawler.settings.get("DATABASE"),
            user=crawler.settings.get("USER"),
            password=crawler.settings.get("PASSWORD"),
            port=crawler.settings.get("PORT")
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, port=self.port, charset='utf8')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        sql = "insert into quotes_t(quotes,author,author_link,tags) values('%s','%s','%s','%s')" \
              % (item['quotes'], item['author'], item['author_link'], item['tags'])
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()
