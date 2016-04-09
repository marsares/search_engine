#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap
import numpy as np
from init import *

#初始化并在内存中建立矩阵,避免多次访问数据库
app = Flask(__name__)
bootstrap = Bootstrap(app)
keywords_len = 30
pages_len = 100
alpha = 0.1
init = Init()
keywords_dict = init.keywords()
pagerank = init.pagerank()
correlation = init.correlation()
init.close_conn()

def get_page(page_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM content WHERE id=?", (page_id,))
    result = cursor.fetchone()
    page = {}
    page['url'] = result[1]
    page['title'] = result[2]
    page['content'] = result[3]
    return page

@app.route('/')
def index():
    return render_template('index.html')

#搜索过程分成三步:
#1.关键字向量和相关性矩阵相乘得到每个页面的相关性得分
#2.每个页面的得分加上pagerank系数
#3.排序返回得分非零的页面
@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        keyword_str = request.form['keyword'].strip()
        if keyword_str != "":
            keywords_list = keyword_str.split(' ')
            keywords_matrix = np.zeros(keywords_len)
            # 1.关键字向量和相关性矩阵相乘得到每个页面的相关性得分
            for keyword in keywords_list:
                if keyword in keywords_dict:
                    keywords_matrix[keywords_dict[keyword]] = 1
            result = np.dot(keywords_matrix, correlation)
            result_with_index = np.zeros((len(result), 2))
            # 2.每个页面的得分加上pagerank系数
            for index in range(len(result)):
                if result[index] != 0:
                    result[index] += alpha*pagerank[index]
                    result_with_index[index][0] = result[index]
                result_with_index[index][1] = index
            # 3.排序返回得分非零的页面
            rank = result_with_index[result_with_index[:, 0].argsort()[::-1]]
            pages = []
            conn = sqlite3.connect('../searchengine.db')
            for index in range(len(rank)):
                if rank[index][0] != 0:
                    page = get_page(rank[index][1], conn)
                    pages.append(page)
            conn.close()
            return render_template('result.html', results=pages)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
