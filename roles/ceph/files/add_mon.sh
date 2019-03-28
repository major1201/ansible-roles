#!/bin/bash

host=$2

mkdir -p /var/lib/ceph/mon/ceph-${host}

# if not bootstrap
if [ "$1" == "False" ]; then
    ceph auth get mon. -o /tmp/ceph.mon.keyring
    ceph mon getmap -o /tmp/monmap
fi

ceph-mon --mkfs -i ${host} --monmap /tmp/monmap --keyring /tmp/ceph.mon.keyring
touch /var/lib/ceph/mon/ceph-${host}/done
chown -R ceph. /var/lib/ceph/mon/ceph-${host}/
