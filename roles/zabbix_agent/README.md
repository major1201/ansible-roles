# Ansible Role: zabbix_agent

An Ansible Role that installs Zabbix agent on Linux.

## Role Variables

```yml
zabbix_server: 127.0.0.1

# zabbix scripts config
zabbix_script_nginx_stub_url: http://127.0.0.1/ngx_status
zabbix_script_phpfpm_status_url: http://127.0.0.1/fpm_status
zabbix_script_mysql_username: username
zabbix_script_mysql_password: password
zabbix_script_mysql_port: 3306
```

## Dependencies

None.
