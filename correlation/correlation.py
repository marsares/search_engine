#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a correlation analysis module '

import sqlite3
import math


class Correlation(object):
    conn = None
    contents = []
    keywords = []
    contents_len = 0
    keywords_len = 0

    def construct_contents(self):
        self.conn = sqlite3.connect('../searchengine.db')
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM content")
        result = cursor.fetchall()
        self.contents_len = len(result)
        if self.contents_len > 0:
            for index in range(self.contents_len):
                self.contents.append(result[index][3])

    def construct_keywords(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM keywords")
        result = cursor.fetchall()
        self.keywords_len = len(result)
        if self.keywords_len > 0:
            for index in range(self.keywords_len):
                self.keywords.append(result[index][1])

    def correlation(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS [correlation]
              ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
              [keyword_id] INTEGER,
              [page_id] INTEGER,
              [correlation] NUMERIC);''')
        self.conn.commit()
        cursor = self.conn.cursor()
        for keyword_index in range(self.keywords_len):
            keyword = self.keywords[keyword_index]
            correlation = []
            dw = 0
            for content_index in range(self.contents_len):
                content = self.contents[content_index]
                if content.count(keyword) != 0:
                    dw += 1
                    correlation.append(float(content.count(keyword)) / len(content))
                else:
                    correlation.append(0)
            for content_index in range(self.contents_len):
                cursor.execute(
                    '''INSERT OR IGNORE INTO [correlation]([keyword_id],[page_id],[correlation]) VALUES(?,?,?);''',
                    (keyword_index, content_index, correlation[content_index] * math.log(self.contents_len*10 / dw)))
        self.conn.commit()
        self.conn.close()

def correlation():
    correlation = Correlation()
    correlation.construct_contents()
    correlation.construct_keywords()
    correlation.correlation()


if __name__ == '__main__':
    correlation()
