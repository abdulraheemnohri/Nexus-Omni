"""
Workflow Engine for v5.0
Handles sequential execution of actions
"""

class WorkflowEngine:
    def __init__(self, ai_engine, plugin_loader):
        self.ai = ai_engine
        self.plugins = plugin_loader

    def execute_workflow(self, workflow):
        """
        workflow: list of dicts with 'type' and 'params'
        """
        results = []
        for step in workflow:
            step_type = step.get('type')
            params = step.get('params', {})

            if step_type == 'ai_process':
                res = self.ai.process(params.get('user_id'), params.get('text'))
                results.append(res)
            elif step_type == 'plugin_execute':
                plugin = self.plugins.get_plugin(params.get('plugin_name'))
                if plugin:
                    res = plugin.execute(params.get('command'), params.get('args'))
                    results.append(res)
                else:
                    results.append(f"Plugin {params.get('plugin_name')} not found")
        return results
