# Ansible Role: keepalived

An Ansible Role that installs keepalived on Linux.

## Role Variables

```yml
keepalived_config: keepalived.conf
keepalived_name: keep1
keepalived_vrid: 11
keepalived_priority: 1 # different hosts should be different, larger priority means higher priority
keepalived_pass: "1111"
keepalived_interface: eth0
keepalived_vips:
  - 192.168.1.100/24 dev eth0
  # - 10.0.0.100/24 dev eth1
keepalived_vroutes: []
  # - "default via 10.0.0.1"
```

## Dependencies

None.
