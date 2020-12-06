
import time
from typing import List

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


    def __init__(self, max_workers=None, timeout: int = 10):
        self.max_workers = max_workers
        self.timeout = timeout
        self.max_depth = 2


    def check_page(self, url: str) -> str:
        """
        Method checks if page exists
        :param timeout:     time to wait until response
        :return:            url if page exists
        """

        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:

            return url


    async def get_data(self, session, url: str):
        """
        Method that fetches data from a server
        :param base_url:    a base url to fetch data
        :return:            data
        """

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            with session.get(url) as response:
                data = response
                print(response.status_code)
                if response.status_code != 200:
                    print("FAILURE::{0}".format(url))
                else:
                    return data, url


    async def get_async_data(self, url: str, depth: int):
        """
        Method to asynchronously get data from url
        :param urls:    list of urls to get data from
        :return:
        """
        #with requests.Session() as session:
        #    with session.get(url) as response:

        response = requests.get(url, timeout=self.timeout)
        print(response.status_code)
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))
        return response, url
        '''
        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            with requests.Session() as session:

                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.get_data,
                        *(session, url)
                    )
                    for url in urls
                ]

                #return await asyncio.gather(*tasks)
                for response, url in await asyncio.gather(*tasks):
                    content = response.text
                    #print(url, depth, content[0])
                    for link in BeautifulSoup(response.text,
                                              parse_only=SoupStrainer('a')):
                        if link.has_attr('href'):
                            print(link['href'])
                yield url, depth, content
                    # with open('workfile.html', 'w') as f:
                    #     f.write(content)
        '''


    def check_urls(self, urls: List[str]):
        """

        :param urls:    list of urls to check
        :return:
        """
        loop = asyncio.get_event_loop()
        print(f'Count of urls before checking: {len(urls)}')
        urls = asyncio.ensure_future(self.check_urls(urls))
        loop.run_until_complete(urls)
        urls = urls.result()
        print(f'Count of urls after checking: {len(urls)}')
        return urls



    def grab(self, base_url: str, depth: int = 0) -> None:
        """
        Method for grubbing pages in depth
        :param base_url:    url for start
        :return:            None
        """

        depth_i = -1
        # Start time counting
        threaded_start = time.time()
        if 0 <= depth <= self.max_depth:
            #urls = [base_url]
            urls = ["https://en.wikipedia.org/wiki/" + str(i) for i in
                              range(50)]

            print("Running threaded:")
            while depth_i != depth:
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = []
                    for url in urls:
                        futures.append(executor.submit(self.get_async_data, *(url, depth)))
                    for feature in futures:
                        print(feature.result())
                depth_i += 1

        else:
            print(f"Max depth should me from 0 to {self.max_depth}!")

        # Stop time counting
        print("Threaded time:", time.time() - threaded_start)


def main():
    spyder = Spyder()
    depth = 0
    base_url = 'https://www.metro-cc.ru/'
    spyder.grab(base_url=base_url, depth=depth)



if __name__ == '__main__':
    #main()
    mem = max(memory_usage(proc=main))
    print("Maximum memory used: {} MiB".format(mem))
