# Ansible Role: shadowsocks

An Ansible Role that installs Shadowsocks on Linux.

## Role Variables

```yml
shadowsocks_user: root
shadowsocks_listen: 0.0.0.0
shadowsocks_timeout: 300
shadowsocks_method: "chacha20-ietf-poly1305"
shadowsocks_port_password:
  "8388": "password"
shadowsocks_tcp_bbr: false
```

## Dependencies

None.
