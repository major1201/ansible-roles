#!/bin/bash

host=$1

ceph auth rm mgr.${host}
