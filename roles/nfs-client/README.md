# Ansible Role: nfs-client

An Ansible Role that installs NFS client on Linux.

## Role Variables

```yml
# nfs_client_mounts exmaple
# nfs_client_mounts:
#   - mountpoint: /mnt
#     opts: ro,_netdev # default rw,_netdev
#     src: nfs.example.com:/exports/myfolder
nfs_client_mounts: []
```

## Dependencies

None.
