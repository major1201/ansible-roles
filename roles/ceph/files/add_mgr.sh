#!/bin/bash

host=$1

mkdir -p /var/lib/ceph/mgr/ceph-${host}
ceph auth get-or-create mgr.${host} mon 'allow profile mgr' osd 'allow *' mds 'allow *' > /var/lib/ceph/mgr/ceph-${host}/keyring
touch /var/lib/ceph/mgr/ceph-${host}/done
chown -R ceph. /var/lib/ceph/mgr/ceph-${host}/
