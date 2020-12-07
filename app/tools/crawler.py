
import time
from typing import List, Dict, Set

import asyncio
import requests
from bs4 import BeautifulSoup, SoupStrainer
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from memory_profiler import memory_usage

#from ..database import



class Spyder(object):
    """
    Spyder class is based on asyncio

    max_workers:    if None, workers = 5*(cpu number)
    max_depth:      max depth for parser
    timeout:        time to wait until response
    urls:           list of urls
    """

    max_workers: int
    max_depth: int
    timeout: int
    urls: List[str]
    urls_to_save: Dict[int, List[str]]


    def __init__(self, max_workers=None, timeout: int = 10):
        self.max_workers = max_workers
        self.timeout = timeout
        self.max_depth = 2


    def get_url_data(self, session, url: str, depth: int):
        """
        Method to asynchronously get data from url
        :param url:    url to get data from
        :return:       data
        """
        with session.get(url) as response:
            html = response.text
            if response.status_code != 200:
                print("FAILURE::{0}".format(url))
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            links = []
            for link in BeautifulSoup(response.text, "html.parser",
                                      parse_only=SoupStrainer('a')):
                if link.has_attr('href'):
                    if 'https:' in link['href']:
                        links.append(link['href'])
            print(depth, title, html[0:15], links[:3])
            # print(self.urls)
            if depth < self.max_depth:
                self.urls_to_save[depth+1] += links
            # TODO: save to DB
            return depth, html[0:15], links, title


    async def get_data_async(self, urls: List[str], depth: int):
        """
        Method to get data from urls async
        :param urls:
        :return:
        """
        urls = list(set(urls))
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            with requests.Session() as session:
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.get_url_data,
                        *(session, url, depth)
                    )
                    for url in urls
                ]

                #for response in await asyncio.gather(*tasks):
                #    print(response)


    def grab(self, base_url: str, depth: int = 0) -> None:
        """
        Method for grubbing pages in depth
        :param base_url:    url for start
        :return:            None
        """
        self.max_depth = depth
        self.urls_to_save = dict([(i, []) for i in range(depth + 1)])

        if 0 <= depth <= self.max_depth:
            self.urls = [base_url]

            with requests.Session() as session:
                self.get_url_data(session, base_url, depth=0)
            print(self.urls_to_save)
            if depth != 0:
                #for depth_i in range(depth+1):
                print(0)
                loop = asyncio.get_event_loop()
                future = asyncio.ensure_future(self.get_data_async(
                                self.urls_to_save[0], 0))
                loop.run_until_complete(future)
                if depth >= 1:
                    loop = asyncio.get_event_loop()
                    future = asyncio.ensure_future(self.get_data_async(
                                    self.urls_to_save[1], 1))
                    loop.run_until_complete(future)
                    if depth == 2:
                        loop = asyncio.get_event_loop()
                        future = asyncio.ensure_future(self.get_data_async(
                                        self.urls_to_save[2], 2))
                        loop.run_until_complete(future)

        else:
            print(f"Max depth should me from 0 to {self.max_depth}!")


def start_crawling(base_url: str, depth: int = 0):

    spyder = Spyder()
    spyder.grab(base_url=base_url, depth=depth)


# start_crawling(base_url='https://lenta.ru', depth=2)
