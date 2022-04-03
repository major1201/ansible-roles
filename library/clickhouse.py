#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import requests
import random
import string

DOCUMENTATION = r'''
---
module: clickhouse

short_description: ClickHouse SQL runner

version_added: "1.0.0"

description: ClickHouse SQL runner

options:
    query:
        description: ClickHouse SQL query to run
        required: true
        type: str
    host:
        description: Indicates the ClickHouse server host
        required: false
        type: str
        default: 127.0.0.1
    port:
        description: Indicates the ClickHouse server HTTP port
        required: false
        type: int
        default: 8123
    user:
        description: ClickHouse user
        required: false
        type: str
        default: default
    password:
        description: ClickHouse password
        required: false
        type: str
        default: ""
    query_id:
        description: ClickHouse query ID
        required: false
        type: str
        default: ""
    query_id_generator:
        description: ClickHouse query ID generator with prefix, query_id_generator: "zhuminjie" => query_id = "zhuminjie_dz83g"
        required: false
        type: str
        default: "ansible"
    format:
        description: Output format
        required: false
        type: str
        default: "TSV"
    extra_params:
        description: Extra params when executing query
        required: false
        type: dict
        default: {}
    timeout:
        description: Request timeout seconds
        required: false
        type: int
        default: 10

requirements:
    - requests

author:
    - major1201@gmail.com
'''

EXAMPLES = r'''
# Execute a simple query with default format
- name: Test a simple query
  clickhouse:
    query: select 1
    format: JSONCompact

- name: Test with a custom query_id
  clickhouse:
    query: select 1
    query_id: zhuminjie_major_hello_world
'''

RETURN = r'''
query_id:
    description: Query ID
    type: str
    returned: success
    sample: 'ansible-zdz3a'
data:
    description: Query data result
    type: complex
    returned: success
    sample: '1\n'
'''


class ClickHouseClient(object):
    def __init__(self, host='127.0.0.1', port=8123, user='default', password='', timeout=10):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout

    def execute(self, query, **params):
        _params = {
            'user': self.user,
            'password': self.password,
            'default_format': 'TSV',
            **params,
        }
        resp = requests.post(
            url='http://{}:{}'.format(self.host, self.port),
            headers={'Content-Type': 'text/plain; charset=utf-8'},
            timeout=self.timeout,
            data=query,
            params=_params,
        )
        resp.raise_for_status()

        if _params['default_format'] in ('JSON', 'JSONCompact'):
            return resp.json()
        return resp.text


def gen_query_id(query_id, query_id_generator) -> str:
    if query_id:
        return query_id
    # postfix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))  # Python 3.6 needed
    postfix = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    return '{}_{}'.format(query_id_generator, postfix)


def run_module():
    module_args = dict(
        query=dict(type='str', required=True),
        host=dict(type='str', required=False, default='127.0.0.1'),
        port=dict(type='int', required=False, default=8123),
        user=dict(type='str', required=False, default='default'),
        password=dict(type='str', required=False, default='', no_log=True),
        query_id=dict(type='str', required=False, default=''),
        query_id_generator=dict(type='str', required=False, default='ansible'),
        format=dict(type='str', required=False, default='TSV'),
        extra_params=dict(type='dict', required=False, default={}),
        timeout=dict(type='int', required=False, default=10),
    )

    result = dict(
        changed=True,
        query_id='',
        data=None,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    ch = ClickHouseClient(
        host=module.params['host'],
        port=module.params['port'],
        user=module.params['user'],
        password=module.params['password'],
        timeout=module.params['timeout'],
    )

    query_id = gen_query_id(module.params['query_id'], module.params['query_id_generator'])
    execute_params = {
        'query_id': query_id,
        'default_format': module.params['format'],
        **module.params['extra_params'],
    }

    try:
        res = ch.execute(module.params['query'], **execute_params)
        result['query_id'] = query_id
        result['data'] = res
        module.exit_json(**result)
    except Exception as e:
        module.fail_json(msg=str(e), **result)


def main():
    run_module()


if __name__ == '__main__':
    main()
