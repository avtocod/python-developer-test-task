import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Function to fetch data from server
def fetch(session, base_url):
    with session.get(base_url) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
        return data

async def get_data_asynchronous():
    urls = ['https://chel.metro-cc.ru/']*10
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            # Set any session parameters here before calling `fetch`
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, url) # Allows us to pass in multiple arguments to `fetch`
                )
                for url in urls
            ]
            for response in await asyncio.gather(*tasks):
                print(response)

def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

main()
