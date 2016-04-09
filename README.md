**Search Engine**
=============
----------
#功能

 - 从起始站点爬取100个网页
 - 选取其中30个关键字，在100个网页内提供这30个关键字的搜索

#运行说明
结构：
 - my_spider
 - searchengine.db
 - pagerank
 - keywords
 - correlation
 - my_web

my_spider：
负责从起始站点爬取网页并把信息存入searchengine.db，在my_spider根目录运行如下命令开始爬取

    scrapy crawl my_spider

pagerank:
负责根据页面之间的指向建立页面的重要性排名

    python pagerank.py

keywords:
负责建立关键字索引

    python keywords.py

correlation:
负责建立关键字和页面的相关性矩阵

    python correlation.py
    
my_web:
基于flask框架搭建的[搜索页面][1],运行如下命令启动

    python my_web.py

  [1]: 127.0.0.1%EF%BC%9A5000