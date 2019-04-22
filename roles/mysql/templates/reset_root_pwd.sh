#! /bin/sh

# --------------------------------------------
# IMPORTANT! Please stop mysqld service first!
# --------------------------------------------

/usr/local/mysql/sbin/mysqld --daemonize --pid-file=/var/mysql/mysqld.pid --user=mysql --skip-grant-tables --skip-networking --log-error

echo "FLUSH PRIVILEGES;" > /tmp/mysqlrst.sql
echo "ALTER USER 'root'@'localhost' IDENTIFIED BY '{{ mysql_root_localhost_pass }}';" >> /tmp/mysqlrst.sql
echo "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '{{ mysql_root_remote_pass }}' WITH GRANT OPTION;" >> /tmp/mysqlrst.sql
echo "FLUSH PRIVILEGES;" >> /tmp/mysqlrst.sql

/usr/local/mysql/bin/mysql -uroot < /tmp/mysqlrst.sql
rm -f /tmp/mysqlrst.sql
kill `cat /var/mysql/mysqld.pid`
