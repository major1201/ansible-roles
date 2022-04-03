from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()
        result = super(ActionModule, self).run(tmp, task_vars)

        args = self._task.args.copy()

        # set default ClickHouse port, user, password
        if 'ch_port' in task_vars:
            args['port'] = task_vars['ch_port']
        if 'ch_user' in task_vars:
            args['user'] = task_vars['ch_user']
        if 'ch_password' in task_vars:
            args['password'] = task_vars['ch_password']

        result.update(
            self._execute_module(module_args=args, task_vars=task_vars),
            _ansible_verbose_always=True)
        return result
