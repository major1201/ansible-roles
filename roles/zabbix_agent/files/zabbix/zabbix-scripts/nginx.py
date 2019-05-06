#! /usr/bin/env python
# encoding: utf-8
from __future__ import division, absolute_import, with_statement, print_function
from utils import num


class NginxStatus(object):
    def __init__(self, url):
        self.url = url

    def get_info(self):
        import requests
        content = requests.get(self.url).content
        return content.split('\n')

    def ping(self):
        import time

        try:
            t_start = time.time()
            self.get_info()
            ping_time = time.time() - t_start
        except:
            from utils import logger
            logger.error_traceback()
            ping_time = 0
        return ping_time > 0

    def accepts(self):
        try:
            content = self.get_info()
            return num.safe_int(content[2].split()[0])
        except:
            return 0

    def handled(self):
        try:
            content = self.get_info()
            return num.safe_int(content[2].split()[1])
        except:
            return 0

    def requests(self):
        try:
            content = self.get_info()
            return num.safe_int(content[2].split()[2])
        except:
            return 0

    def connections_active(self):
        try:
            content = self.get_info()
            return num.safe_int(content[0].split()[-1])
        except:
            return 0

    def connections_reading(self):
        try:
            content = self.get_info()
            return num.safe_int(content[3].split()[1])
        except:
            return 0

    def connections_writing(self):
        try:
            content = self.get_info()
            return num.safe_int(content[3].split()[3])
        except:
            return 0

    def connections_waiting(self):
        try:
            content = self.get_info()
            return num.safe_int(content[3].split()[5])
        except:
            return 0


def main():
    import common
    from utils import setting, argparser

    common.initialize()
    parser = argparser.StringLtdArgParser(
        'ping', 'accepts', 'handled', 'requests', 'connections_active',
        'connections_reading', 'connections_writing', 'connections_waiting'
    )
    arg = parser.get_string_arg()
    ns = NginxStatus(setting.conf.get('nginx').get('stub_url'))
    print(ns.__getattribute__(arg)())


if __name__ == "__main__":
    main()
