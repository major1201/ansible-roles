# Ansible Role: common

An Ansible Role that installs common packages and configurations on Linux.

## Role Variables

```yml
authkey_public: ""  # public key file
authkey_private: ""  # private key file
hosts_file: hosts
hosts_marker: "# {mark} HOSTS BLOCK"
dns_servers:
  - 202.96.209.5
  - 202.96.209.133
hostname_resolve_ip: 127.0.0.1
yumrepo_mirrors_url: https://mirrors.ustc.edu.cn
debian_sources_url: https://mirrors.ustc.edu.cn/debian/
debian_sources_security_url: https://mirrors.ustc.edu.cn/debian-security/
ubuntu_sources_url: https://mirrors.ustc.edu.cn/ubuntu/
sysctl_file: sysctl.conf
```

## Dependencies

None.
