#! /usr/bin/env python
# encoding: utf-8
from __future__ import division, absolute_import, with_statement, print_function
from utils import num


class PhpFpmStatus(object):
    def __init__(self, url):
        self.url = url + '?json'

    def get_info(self):
        import requests
        content = requests.get(self.url).content
        return content.split('\n')

    def get_status(self, status):
        import requests
        import json
        content = requests.get(self.url).content
        obj = json.loads(content)
        val = obj.get(status.replace('_', ' '), '')
        return num.safe_int(val, val)


def main():
    import common
    from utils import setting, argparser

    common.initialize()
    parser = argparser.StringLtdArgParser(
        'pool', 'process_manager', 'start_time', 'start_since', 'accepted_conn', 'listen_queue', 'max_listen_queue',
        'listen_queue_len', 'idle_processes', 'active_processes', 'total_processes', 'max_active_processes',
        'max_children_reached', 'slow_requests'
    )
    arg = parser.get_string_arg()
    ns = PhpFpmStatus(setting.conf.get('php-fpm').get('status_url'))
    print(ns.get_status(arg))


if __name__ == "__main__":
    main()
