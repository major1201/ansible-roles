# Ansible Role: docker

An Ansible Role that installs Docker on Linux.

## Role Variables

```yml
# docker config
docker_bip: "192.168.0.1/24"
docker_dns:
  - 223.5.5.5
  - 223.6.6.6
docker_registry_insecure: false
docker_registry_mirrors:
  - "https://docker.mirrors.ustc.edu.cn"
```

## Dependencies

None.
