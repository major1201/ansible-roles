# encoding: utf-8
from __future__ import division, absolute_import, with_statement, print_function


def initialize():
    import os.path

    # init setting
    from utils import setting
    with open(os.path.join(os.path.dirname(__file__), "conf.yml")) as _f:
        setting.load(_f)

    # init logger
    from utils import logger
    import logging
    logger.initialize()
    # turn off annoying log in requests
    logging.getLogger("requests").setLevel(logging.WARNING)
