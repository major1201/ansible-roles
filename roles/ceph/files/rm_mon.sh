#!/bin/bash

host=$1

ceph mon remove ${host}
