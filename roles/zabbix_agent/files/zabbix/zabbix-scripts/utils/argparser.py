# encoding: utf-8
from __future__ import division, absolute_import, with_statement, print_function


class BaseArgParser(object):
    pass


class StringLtdArgParser(BaseArgParser):
    def __init__(self, *ltd_args):
        from utils import setting
        import argparse

        self._ltd_args = ltd_args
        parser = argparse.ArgumentParser(prog=setting.conf.get('project_name'), description="Zabbix Script Bundle",
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('choice', metavar='choice', choices=self._ltd_args,
                            help='choose one in :' + ', '.join(self._ltd_args))
        self._args = parser.parse_args()

    def get_string_arg(self):
        return self._args.choice
