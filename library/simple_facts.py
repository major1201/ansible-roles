# encoding: utf-8
from __future__ import division, absolute_import, with_statement, print_function

import os
import sys
import platform
import stat
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import facts


def is_executable(path):
    """is the given path executable?

    Limitations:
    * Does not account for FSACLs.
    * Most times we really want to know "Can the current user execute this
      file"  This function does not tell us that, only if an execute bit is set.
    """
    # These are all bitfields so first bitwise-or all the permissions we're
    # looking for, then bitwise-and with the file's mode to determine if any
    # execute bits are set.
    return (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & os.stat(path)[stat.ST_MODE]


def get_bin_path(arg, required=False, opt_dirs=[]):
    """
    find system executable in PATH.
    Optional arguments:
       - required:  if executable is not found and required is true, fail_json
       - opt_dirs:  optional list of directories to search in addition to PATH
    if found return full path; otherwise return None
    """
    sbin_paths = ['/sbin', '/usr/sbin', '/usr/local/sbin']
    paths = []
    for d in opt_dirs:
        if d is not None and os.path.exists(d):
            paths.append(d)
    paths += os.environ.get('PATH', '').split(os.pathsep)
    bin_path = None
    # mangle PATH to include /sbin dirs
    for p in sbin_paths:
        if p not in paths and os.path.exists(p):
            paths.append(p)
    for d in paths:
        if not d:
            continue
        path = os.path.join(d, arg)
        if os.path.exists(path) and is_executable(path):
            bin_path = path
            break
    if required and bin_path is None:
        print('Failed to find required executable %s' % arg)
    return bin_path


class SimpleFacts(object):
    PKG_MGRS = [{'path': '/usr/bin/yum', 'name': 'yum'},
                {'path': '/usr/bin/dnf', 'name': 'dnf'},
                {'path': '/usr/bin/apt-get', 'name': 'apt'},
                {'path': '/usr/bin/zypper', 'name': 'zypper'},
                {'path': '/usr/sbin/urpmi', 'name': 'urpmi'},
                {'path': '/usr/bin/pacman', 'name': 'pacman'},
                {'path': '/bin/opkg', 'name': 'opkg'},
                {'path': '/usr/pkg/bin/pkgin', 'name': 'pkgin'},
                {'path': '/opt/local/bin/pkgin', 'name': 'pkgin'},
                {'path': '/opt/local/bin/port', 'name': 'macports'},
                {'path': '/usr/local/bin/brew', 'name': 'homebrew'},
                {'path': '/sbin/apk', 'name': 'apk'},
                {'path': '/usr/sbin/pkg', 'name': 'pkgng'},
                {'path': '/usr/sbin/swlist', 'name': 'SD-UX'},
                {'path': '/usr/bin/emerge', 'name': 'portage'},
                {'path': '/usr/sbin/pkgadd', 'name': 'svr4pkg'},
                {'path': '/usr/bin/pkg', 'name': 'pkg'},
                {'path': '/usr/bin/xbps-install', 'name': 'xbps'},
                {'path': '/usr/local/sbin/pkg', 'name': 'pkgng'},
                ]

    def __init__(self):
        self.facts = {}
        self.get_platform_facts()
        self.facts.update(facts.Distribution(None).populate())
        self.get_pkg_mgr_facts()
        self.get_service_mgr_facts()
        self.get_python_facts()

    def populate(self):
        return self.facts

    def get_platform_facts(self):
        self.facts['system'] = platform.system()
        self.facts['kernel'] = platform.release()
        self.facts['machine'] = platform.machine()
        self.facts['python_version'] = platform.python_version()
        self.facts['hostname'] = platform.node().split('.')[0]
        self.facts['nodename'] = platform.node()

    def get_pkg_mgr_facts(self):
        if self.facts['system'] == 'OpenBSD':
                self.facts['pkg_mgr'] = 'openbsd_pkg'
        else:
            self.facts['pkg_mgr'] = 'unknown'
            for pkg in SimpleFacts.PKG_MGRS:
                if os.path.exists(pkg['path']):
                    self.facts['pkg_mgr'] = pkg['name']

    def is_systemd_managed(self):
        # tools must be installed
        if get_bin_path('systemctl'):

            # this should show if systemd is the boot init system, if checking init faild to mark as systemd
            # these mirror systemd's own sd_boot test http://www.freedesktop.org/software/systemd/man/sd_booted.html
            for canary in ["/run/systemd/system/", "/dev/.run/systemd/", "/dev/.systemd/"]:
                if os.path.exists(canary):
                    return True
        return False

    def get_service_mgr_facts(self):
        # try various forms of querying pid 1
        proc_1 = facts.get_file_content('/proc/1/comm')
        if proc_1 is None:
            rc, proc_1, err = self.module.run_command("ps -p 1 -o comm|tail -n 1", use_unsafe_shell=True)
        else:
            proc_1 = os.path.basename(proc_1)

        # The ps command above may return "COMMAND" if the user cannot read /proc, e.g. with grsecurity
        if proc_1 == "COMMAND\n":
            proc_1 = None

        if proc_1 is not None:
            proc_1 = facts.to_native(proc_1)
            proc_1 = proc_1.strip()

        if proc_1 is not None and (proc_1 == 'init' or proc_1.endswith('sh')):
            # many systems return init, so this cannot be trusted, if it ends in 'sh' it probalby is a shell in a container
            proc_1 = None

        # if not init/None it should be an identifiable or custom init, so we are done!
        if proc_1 is not None:
            self.facts['service_mgr'] = proc_1

        # start with the easy ones
        elif self.facts['distribution'] == 'MacOSX':
            # FIXME: find way to query executable, version matching is not ideal
            if facts.LooseVersion(platform.mac_ver()[0]) >= facts.LooseVersion('10.4'):
                self.facts['service_mgr'] = 'launchd'
            else:
                self.facts['service_mgr'] = 'systemstarter'
        elif 'BSD' in self.facts['system'] or self.facts['system'] in ['Bitrig', 'DragonFly']:
            # FIXME: we might want to break out to individual BSDs
            self.facts['service_mgr'] = 'bsdinit'
        elif self.facts['system'] == 'AIX':
            self.facts['service_mgr'] = 'src'
        elif self.facts['system'] == 'SunOS':
            # FIXME: smf?
            self.facts['service_mgr'] = 'svcs'
        elif self.facts['system'] == 'Linux':
            if self.is_systemd_managed():
                self.facts['service_mgr'] = 'systemd'
            elif get_bin_path('initctl') and os.path.exists("/etc/init/"):
                self.facts['service_mgr'] = 'upstart'
            elif os.path.realpath('/sbin/rc') == '/sbin/openrc':
                self.facts['service_mgr'] = 'openrc'
            elif os.path.exists('/etc/init.d/'):
                self.facts['service_mgr'] = 'sysvinit'

        if not self.facts.get('service_mgr', False):
            # if we cannot detect, fallback to generic 'service'
            self.facts['service_mgr'] = 'service'

    def get_python_facts(self):
        self.facts['python'] = {
            'version': {
                'major': sys.version_info[0],
                'minor': sys.version_info[1],
                'micro': sys.version_info[2],
                'releaselevel': sys.version_info[3],
                'serial': sys.version_info[4]
            },
            'version_info': list(sys.version_info),
            'executable': sys.executable
        }
        try:
            self.facts['python']['type'] = sys.subversion[0]
        except AttributeError:
            self.facts['python']['type'] = None


def main():
    mdl = AnsibleModule(argument_spec={})
    simple_facts = SimpleFacts().populate()
    for (k, v) in simple_facts.items():
        simple_facts['ansible_' + k] = simple_facts.pop(k)
    mdl.exit_json(changed=False, ansible_facts=simple_facts)


if __name__ == '__main__':
    main()
