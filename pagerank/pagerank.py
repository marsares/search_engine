#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a page rank module '

import sqlite3
import numpy as np

class PageRank(object):

    dict = {}
    conn = None
    matrix = None
    len = 0
    a = 0.001


    def construct_dict(self):
        self.conn = sqlite3.connect('../searchengine.db')
        cursor = self.conn.cursor()
        cursor.execute("select * from content")
        result = cursor.fetchall()
        self.len = len(result)
        if self.len > 0:
            for index in range(self.len):
                self.dict[result[index][1]] = index
                cursor.execute("update content set id=? where url=?", (index, result[index][1]))
        self.conn.commit()

    def construct_matrix(self):
        self.matrix = np.zeros([self.len, self.len], np.float)
        cursor = self.conn.cursor()
        cursor.execute("select * from link")
        result = cursor.fetchall()
        if len(result) > 0:
            for index in range(len(result)):
                if result[index][1] in self.dict and result[index][2] in self.dict:
                    start = self.dict[result[index][1]]
                    dist = self.dict[result[index][2]]
                    self.matrix[dist][start] += 1

    def caculate_pagerank(self):
        rank = np.ones(self.len)/self.len
        rank = rank.reshape((self.len, 1))
        matrix = np.ones((self.len, self.len))*self.a/self.len+self.matrix*(1-self.a)
        for x in range(10):
            rank = np.dot(matrix, rank)
        rank = rank/10e17
        self.conn.execute('''CREATE TABLE IF NOT EXISTS [pagerank]
            ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
             [rank] NUMERIC);''')
        self.conn.commit()
        cursor = self.conn.cursor()
        for index in range(len(rank)):
            cursor.execute("INSERT INTO pagerank VALUES (?,?);", (index, rank[index][0]))
        self.conn.commit()
        self.conn.close()

def pagerank():
    pagerank = PageRank()
    pagerank.construct_dict()
    pagerank.construct_matrix()
    pagerank.caculate_pagerank()

if __name__ == '__main__':
    pagerank()