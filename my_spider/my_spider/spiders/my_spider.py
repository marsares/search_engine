import scrapy
import re
from bs4 import BeautifulSoup, Comment
from .. import items

class MySpider(scrapy.Spider):

    def extract_contents(self, body):
        soup=BeautifulSoup(body, "html5lib")
        [script.extract() for script in soup.find_all('script')]
        [comment.extract() for comment in soup.find_all(text=lambda text:isinstance(text, Comment))]
        return "".join(soup.get_text().split())

    def extract_title(self, body):
        soup = BeautifulSoup(body, "html5lib")
        return soup.title.string

    def extract_links(self, body):
        index = "http://www.cst.zju.edu.cn/"
        soup = BeautifulSoup(body, "html5lib")
        links = []
        for link in soup.find_all('a'):
            if link['href'] == 'index.php' or link['href'] == 'http://www.cst.zju.edu.cn/index.php':
                links.append('http://www.cst.zju.edu.cn/')
            elif re.match(r'http://', link['href']):
                links.append(link['href'])
            elif not re.match(r'#', link['href']):
                links.append(index+link['href'])
        return links

    count = 0
    name = "my_spider"
    allowed_domains = ["www.cst.zju.edu.cn"]
    start_urls = [
        "http://www.cst.zju.edu.cn/"
    ]
    visited = set(start_urls)

    def parse(self, response):
        page = items.PageItem()
        page['title'] = self.extract_title(response.body)
        page['url'] = response.url
        page['content'] = self.extract_contents(response.body)
        page['links'] = self.extract_links(response.body)
        for link in page['links']:
            if self.count < 113:
                self.count += 1
                if link not in self.visited:
                    self.visited.add(link)
                    yield scrapy.Request(link, callback=self.parse)
        yield page
