#!/bin/bash

host=$1

mkdir -p /var/lib/ceph/mds/ceph-${host}
ceph-authtool --create-keyring /var/lib/ceph/mds/ceph-${host}/keyring --gen-key -n mds.${host}
ceph auth add mds.${host} osd "allow rwx" mds "allow" mon "allow profile mds" -i /var/lib/ceph/mds/ceph-${host}/keyring
touch /var/lib/ceph/mds/ceph-${host}/done
chown -R ceph. /var/lib/ceph/mds/ceph-${host}/
