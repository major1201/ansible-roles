# Ansible Role: ceph-client

An Ansible Role that installs Ceph client on Linux.

## Role Variables

```yml
ceph_uuid: 62fad2ac-5ad3-47bb-9dde-9ded449559f2
ceph_repo: ceph.repo
ceph_conf: ceph.conf
ceph_client_keyrings: []

# ceph_client_rbdmap example:
# ceph_client_rbdmap:
#   - pool: mypool
#     image: myimage
#     user: user1
#     mountpoint: /mnt
#     filesystem: ext4
ceph_client_rbdmap: []

# ceph_client_fs example:
# ceph_client_fs:
#   - fs_addr: 10.128.247.14:6789:/
#     mountpoint: /mnt
#     user: user1
#     secret: AQAsZwJbjlKsERAA1rhrRSlSKOWfsIFXZNjyQg==
ceph_client_fs: []
```

## Dependencies

None.
