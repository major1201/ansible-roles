#/bin/bash

/usr/local/mysql/bin/mysql -h{{ zabbix_proxy_dbhost }} -P{{ zabbix_proxy_dbport }} -u{{ zabbix_proxy_dbuser }} -p"{{ zabbix_proxy_dbpassword }}" {{ zabbix_proxy_dbname }} < /tmp/schema.sql
