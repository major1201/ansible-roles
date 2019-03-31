#! /usr/bin/env python
# encoding: utf-8
from __future__ import division, absolute_import, with_statement, print_function
import sys
import argparse

__version__ = '0.1a'
PY2 = sys.version_info[0] == 2


def serve(listen_addr, listen_port, echo_str):
    if PY2:
        from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    else:
        from http.server import BaseHTTPRequestHandler, HTTPServer

    echo_str = echo_str if PY2 else bytes(echo_str.encode('utf-8'))
    h = BaseHTTPRequestHandler
    h.do_GET = lambda r: r.send_response(200) or r.end_headers() or r.wfile.write(echo_str)
    s = HTTPServer((listen_addr, listen_port), h)
    s.serve_forever()


def reg_ip(s):
    import re

    if re.match('^(([2][5][0-5]|[2][0-4][0-9]|[1][0-9]{2}|[1-9][0-9]|[0-9])[.]){3}([2][5][0-5]|[2][0-4][0-9]|[1][0-9]{2}|[1-9][0-9]|[0-9])$', s):
        return s
    else:
        raise argparse.ArgumentTypeError(s + " can't be parsed as IP")


def main():
    parser = argparse.ArgumentParser(prog='quichttp', description='Quickly build an Http server for testing usage.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-a', '--address', dest='address', type=reg_ip, default='0.0.0.0', help='listen address')
    parser.add_argument('-p', '--port', dest='port', type=int, default=80, help='listen port')
    parser.add_argument('-e', '--echo', dest='echo', default='hello', help='echo string')
    _args = parser.parse_args()
    print('Serving HTTP on ' + _args.address + ':' + str(_args.port) + '...')
    serve(_args.address, _args.port, _args.echo)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass
