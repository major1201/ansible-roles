# Ansible Role: zabbix_proxy

An Ansible Role that installs Zabbix proxy on Linux.

## Role Variables

```yml
zabbix_proxy_proxymode: 0
zabbix_proxy_server: 127.0.0.1
zabbix_proxy_serverport: 10051
zabbix_proxy_hostname: Zabbix proxy
zabbix_proxy_listenport: 10051
zabbix_proxy_logfile: /var/log/zabbix/zabbix_proxy.log
zabbix_proxy_dbhost: localhost
zabbix_proxy_dbname: ""
zabbix_proxy_dbuser: ""
zabbix_proxy_dbpassword: ""
zabbix_proxy_dbsocket: /tmp/mysql.sock
zabbix_proxy_dbport: 3306
# 当数据发送到Server，还要在本地保留多少小时
zabbix_proxy_localbuffer: 0
# 当数据没有发送到Server，在本地保留多少小时
zabbix_proxy_offlinebuffer: 1
# 心跳检测代理在Server的可用性
zabbix_proxy_heartbeatfrequency: 60
# 代理多久从Server获取一次配置变化，默认3600秒
zabbix_proxy_configfrequency: 3600
# 代理收集到数据后，多久向Server发送一次
zabbix_proxy_datasenderfrequency: 1
```

## Dependencies

None.
