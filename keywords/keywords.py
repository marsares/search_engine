#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a key words module '

import sqlite3

keywords = [u'实训', u'专业', u'研究生', u'信息', u'通知', u'文件', u'实习',
            u'就业', u'服务', u'工作', u'合作', u'下载', u'招生', u'管理', u'学历',
            u'校园', u'教学', u'创新基地', u'企业', u'注册', u'夏令营', u'讲座', u'公司',
            u'项目', u'培训', u'科研', u'证书', u'论文', u'评奖', u'活动']

def generate():
    conn = sqlite3.connect('../searchengine.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS [keywords]
        ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
         [keyword] TEXT);''')
    conn.commit()
    cursor = conn.cursor()
    for index in range(len(keywords)):
        cursor.execute('''INSERT OR IGNORE INTO [keywords] ([id],[keyword]) VALUES (?,?);''', (index, keywords[index]))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    generate()