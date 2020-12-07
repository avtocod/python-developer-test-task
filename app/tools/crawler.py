
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
        # with requests.Session() as session:
        # with session.get(url) as response:

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
            # print(depth, html[0:15], links, title)
            # print(self.urls)
            self.urls_to_save[depth] += links
            # TODO: save to DB
            return depth, html[0:15], links, title


    async def get_data_async(self, urls: List[str], depth: int):
        """

        :param urls:
        :return:
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            with requests.Session() as session:
                # Set any session parameters here before calling `fetch`
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.get_url_data,
                        *(session, url, depth)
                        # Allows us to pass in multiple arguments to `fetch`
                    )
                    for url in urls
                ]

                for response in await asyncio.gather(*tasks):
                    print(response)


    def grab(self, base_url: str, depth: int = 0) -> None:
        """
        Method for grubbing pages in depth
        :param base_url:    url for start
        :return:            None
        """
        self.urls_to_save = dict([(i, []) for i in range(depth + 1)])

        depth_i = -1
        if 0 <= depth <= self.max_depth:
            self.urls = [base_url]

            with requests.Session() as session:
                self.get_url_data(session, base_url, depth=0)
            print(self.urls_to_save)
            if depth != 0:
                #for depth_i, links in self.urls_to_save.items():
                for depth_i in range(depth):
                    print(depth_i)
                    loop = asyncio.get_event_loop()
                    future = asyncio.ensure_future(self.get_data_async(
                                    self.urls_to_save[depth_i], depth_i))
                    loop.run_until_complete(future)

        else:
            print(f"Max depth should me from 0 to {self.max_depth}!")


def main():

    spyder = Spyder()
    depth = 1
    base_url = 'https://www.metro-cc.ru/'
    spyder.grab(base_url=base_url, depth=depth)


if __name__ == '__main__':
    # main()
    # Start time counting
    start_time = time.time()
    mem = max(memory_usage(proc=main))
    # Stop time counting
    execution_time = time.time() - start_time
    print(f"ok, execution time: {execution_time:.3f}s, peak memory usage: {mem} Mb")
