# Ansible Role: Ceph

An Ansible Role that installs Ceph on Linux.

## Role Variables

```yml
ceph_repo: ceph.repo  # ceph repo file
ceph_uuid: 62fad2ac-5ad3-47bb-9dde-9ded449559f2  # ceph cluster uuid
ceph_conf: ceph.conf  # ceph config file
ceph_admin_keyring_local: "{{ custom_config_dir }}ceph.client.admin.keyring"
ceph_bootstrap_osd_keyring_local: "{{ custom_config_dir }}ceph.bootstrap.osd.keyring"
ceph_bootstrap: false  # is bootstrap host or not
ceph_mon: false  # is ceph monitor or not
ceph_mon_init_address: 192.168.1.101  # ceph monitor init address
ceph_mgr: false  # is ceph manager or not
ceph_mds: false  # is ceph mds or not
```

## Dependencies

None.
