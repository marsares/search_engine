import sqlite3
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MySpiderPipeline(object):

    conn = None

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO [content]([url], [title], [content]) VALUES(?, ?, ?);''',
                       (item["url"], item["title"], item["content"]))
        for link in item["links"]:
            cursor.execute('''INSERT OR IGNORE INTO [link]([start],[dist]) VALUES(?,?);''', (item["url"], link))
        self.conn.commit()
        cursor.close()
        return item

    def open_spider(self, spider):
        self.conn = sqlite3.connect('../../searchengine.db')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS [content]
                             ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
                              [url] TEXT,
                              [title] TEXT,
                              [content] TEXT);''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS [link]
                             ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
                              [start] TEXT,
                              [dist] TEXT);''')
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
