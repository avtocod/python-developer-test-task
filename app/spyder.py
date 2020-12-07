import os
import sys
import time
import argparse
from memory_profiler import memory_usage
import logging
import logging.config
from tools.crawler import start_crawling


def parse_arguments(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('command', type=str, default='load',
                        help='command: load from web or get from DB')
    parser.add_argument('link', type=str, default='https://lenta.ru',
                        help='link dor web site')
    parser.add_argument('--depth', type=int, default=2,
                        help='web site crawl depth')
    parser.add_argument('--logs_dir', type=str, default='logs',
                        help="path to directory with logs")
    parser.add_argument('--logging_yaml', type=str, default='./app/logging.yaml',
                        help="path to yaml logger config")

    return parser.parse_args()


def main(args):

    print(os.getcwd())
    print(os.listdir(os.getcwd()))

    if not os.path.exists(args.logs_dir):
        os.makedirs(args.logs_dir)

    # logging.config.fileConfig(args.logging_yaml)

    if len(sys.argv) >= 3:
        command = sys.argv[1]
        link = sys.argv[2]
        depth = args.depth

        if command == 'load':
            logging.info('load')
            print('load')
            start_time = time.time()
            #start_crawling(base_url=link, depth=0)
            mem = max(memory_usage(proc=start_crawling(base_url=link,
                                                       depth=depth)))
            # Stop time counting
            execution_time = time.time() - start_time
            print(f"ok, execution time: {execution_time:.3f}s, peak memory usage: {mem} Mb")
        elif command == 'get':
            print('get')
        else:
            print("There must be at least command arg and website link!" + \
                  "Example: 'spider.py load http://www.vesti.ru/ --depth 2'")
            logging.error("There must be at least command and website link!")
            logging.info("Ex: 'spider.py load http://www.vesti.ru/ --depth 2")

        print(link)

    else:
        print("There must be at least command arg and website link!" + \
              "Example: 'spider.py load http://www.vesti.ru/ --depth 2'")
        logging.error("There must be at least command arg and website link!")
        logging.info("Example: 'spider.py load http://www.vesti.ru/ --depth 2")


if __name__ == '__main__':
    main(parse_arguments(sys.argv[2:]))
