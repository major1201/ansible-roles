#! /usr/bin/env python
# encoding=utf-8
import sys
import datetime
import string
import subprocess

COMMAND = "rpm -qa --qf '%{INSTALLTIME} %{NAME}-%{VERSION}-%{RELEASE}:  %{SUMMARY}\n' | sort -nr"


def is_none(s):
    return s is None


def is_empty(s):
    return is_none(s) or len(str(s)) == 0


def is_blank(s):
    if is_empty(s):
        return True
    for char in s:
        if char not in string.whitespace:
            return False
    return True


if __name__ == "__main__":
    process = subprocess.Popen([COMMAND], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout.readlines():
        if is_blank(line): continue
        try:
            item_arr = line.split(" ")
            time = datetime.datetime.fromtimestamp(int(item_arr[0])).strftime("%Y-%m-%d %H:%M:%S")
            sys.stdout.write("[" + time + "] " + " ".join(item_arr[1:]))
        except:
            break
