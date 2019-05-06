#! /usr/bin/env python
# encoding: utf-8
from __future__ import division, absolute_import, with_statement, print_function
from utils import setting


class MysqlStatus(object):
    def __init__(self, cmd, *args):
        # init db
        from utils.dao import context
        context.DBContext.initialize(context.DBConfig.from_dict(setting.conf.get("mysql")))

        self.cmd = cmd
        self.args = args

    @staticmethod
    def ping():
        import time
        from utils.dao.context import DBContext
        st = time.time()
        try:
            DBContext().execute('select 1')
            return bool(time.time() - st)
        except:
            return 0

    @staticmethod
    def status(statkey):
        from utils import num
        from utils.dao.context import DBContext
        try:
            ret = DBContext().create_sql_query('show global status like :statkey', statkey=statkey).fetch(True)
            val = ret[0]['value']
            return num.safe_int(val, val)
        except:
            from utils import logger
            logger.error_traceback()
            return -1

    def get_val(self):
        if self.cmd == 'ping':
            return self.ping()
        elif self.cmd == 'status':
            return self.status(self.args[0])


def main():
    import common
    common.initialize()

    import argparse
    parser = argparse.ArgumentParser(prog=setting.conf.get('project_name'), description="Zabbix Script Bundle",
                                     formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers()
    # cmd: ping
    parser_ping = subparsers.add_parser('ping')
    parser_ping.add_argument('cmd', action='store_const', const='ping')
    # cmd: status
    parser_status = subparsers.add_parser('status')
    parser_status.add_argument('cmd', action='store_const', const='status')
    parser_status.add_argument('statkey', metavar='status key')

    args = parser.parse_args()

    print(MysqlStatus(args.cmd, getattr(args, 'statkey', None)).get_val())


if __name__ == "__main__":
    main()
