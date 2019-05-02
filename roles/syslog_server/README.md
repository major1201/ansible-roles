# Ansible Role: syslog_server

An Ansible Role that installs syslog server(syslog-ng) on Linux.

## Role Variables

```yml
# log_path must end with a slash("/")
log_path: /var/log/hosts/
max_connections: 50
```

## Dependencies

None.
