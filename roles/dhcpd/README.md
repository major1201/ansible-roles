# Ansible Role: dhcpd

An Ansible Role that installs DHCP server on Linux.

## Role Variables

```yml
dns_servers: "8.8.8.8, 8.8.4.4"  # dns servers
dhcpd_conf_list:  # dhcp config files
  - name: dhcpd.conf
    src_path: dhcpd.conf
```

## Dependencies

None.
