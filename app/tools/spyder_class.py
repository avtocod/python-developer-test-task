import scrapy
import requests
from typing import List, Dict


class Spider(scrapy.Spider):
    """
    Class Spyder is a  class
    that simplifies web scraping


    """
    name: str = 'SpiderClass'


    def __init__(self):
        super().__init__()


    def start_requests(self, urls: List[str]) -> scrapy.Request:
        responses = []
        for url in urls:
            response = scrapy.Request(url=url, callback=self.callback)
            responses.append(response)
            print(response.follow(href, self.parse))
            for href in response.css('a::attr(href)'):
                self.callback(response)


    def callback(self, response):
        name = response.url.split('/')[-1]
        filename = f'{name}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'filename {filename} saved')
        print(f'filename {filename} saved')


    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').get()}

        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)



import scrapy

class LinkCheckerSpider(scrapy.Spider):
    name = 'link_checker'
    allowed_domains = ['www.example.com']
    start_urls = ['http://www.example.com/']

    def parse(self, response):
        """ Main function that parses downloaded pages """
        # Print what the spider is doing
        print(response.url)
        # Get all the <a> tags
        a_selectors = response.xpath("//a")
        # Loop on each tag
        for selector in a_selectors:
            # Extract the link text
            text = selector.xpath("text()").extract_first()
            # Extract the link href
            link = selector.xpath("@href").extract_first()
            # Create a new Request object
            request = response.follow(link, callback=self.parse)
            # Return it thanks to a generator
            yield request

'''
spyder = Spider()
#response = requests.get('https://api.github.com/events')
#print(spyder.start_requests(['https://www.metro-cc.ru/']))
print(spyder.start_requests(['https://yourgithub.com']))

'''
