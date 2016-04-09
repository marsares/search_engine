import sqlite3
import numpy as np

class Init(object):
    conn = None
    keywords_len = 30
    pages_len = 100

    def keywords(self):
        self.conn = sqlite3.connect('../searchengine.db')
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM keywords")
        result = cursor.fetchall()
        dict = {}
        if len(result) > 0:
            for index in range(len(result)):
                dict[result[index][1]] = result[index][0]
        return dict

    def pagerank(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pagerank")
        result = cursor.fetchall()
        list = []
        if len(result) > 0:
            for index in range(len(result)):
                list.append(result[index][1])
        return list

    def correlation(self):
        matrix = np.zeros((self.keywords_len, self.pages_len))
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM correlation")
        result = cursor.fetchall()
        if len(result) > 0:
            for index in range(len(result)):
                keyword_id = result[index][1]
                page_id = result[index][2]
                correlation = result[index][3]
                matrix[keyword_id][page_id] = correlation
        return matrix

    def close_conn(self):
        self.conn.close()