import sys
import argparse
import os
import logging
import logging.config
from typing import List

def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('load', type=str, default=None)
    parser.add_argument('get', type=str, default=None)
    parser.add_argument('--depth', type=int, default=2,
                        help='web site crawl depth')
    parser.add_argument('-n', type=int, default=2,
                        help='web site crawl depth')
    parser.add_argument('--logs_dir', type=str, default='/logs/',
                        help="path to directory with logs")
    parser.add_argument('--logging_yaml', type=str, default='logging.yaml',
                        help="path to yaml logger config")

    return parser.parse_args()


def main(args):

    if not os.path.exists(args.logs_dir):
        os.makedirs(args.logs_dir)

    logging.config.fileConfig(args.logging_yaml)

    if len(sys.argv) >= 3:
        command = sys.argv[1]

        if command == 'load':
            print('load')
        elif command == 'get':
            print('get')
        else:
            print("There must be at least command arg and website link!" + \
                  "Example: 'spider.py load http://www.vesti.ru/ --depth 2'")
            logging.error("There must be at least command and website link!")
            logging.info("Ex: 'spider.py load http://www.vesti.ru/ --depth 2")

    else:
        print("There must be at least command arg and website link!" + \
              "Example: 'spider.py load http://www.vesti.ru/ --depth 2'")
        logging.error("There must be at least command arg and website link!")
        logging.info("Example: 'spider.py load http://www.vesti.ru/ --depth 2")


if __name__ == '__main__':
    main(args=parse_arguments(sys.argv[2:]))
