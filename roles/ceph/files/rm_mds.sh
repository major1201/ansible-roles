#!/bin/bash

host=$1

ceph auth rm mds.${host}
