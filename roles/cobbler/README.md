# Ansible Role: cobbler

An Ansible Role that installs cobbler on Linux.

## Role Variables

```yml
# use `openssl passwd -1 -salt 'random-phrase-here' 'your-password-here'` to generate the crypted password
cobbler_default_password: "$1$fdsafb$9xStxf/QuHBmtKrxC7/j./"  # 111
cobbler_subnet: "192.168.1.0"
cobbler_netmask: "255.255.255.0"
cobbler_ip_range: "192.168.1.100 192.168.1.254"
cobbler_routers: "192.168.1.5"
cobbler_dns_servers: "192.168.1.1"
```

## Dependencies

None.
