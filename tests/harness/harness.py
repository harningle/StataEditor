"""Test harness, installed as a package of its own by tests/run_tests.py

It copies the console to <DATA>/console.log, checks StataEditor from inside Sublime Text, and
writes what it found to <DATA>/results.json for `run_tests.py` to judge. It must stay Python 3.3
compatible for ST3.
"""
import json
import os
import sys
import time
import traceback

import sublime

# sublime.packages_path() is empty at import time in ST3, so use `__file__`
DATA = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONSOLE_LOG = os.path.join(DATA, 'console.log')
FIXTURES = os.path.join(DATA, 'fixtures')
PLUGINS = ('StataEditor.StataEditorPlugin', 'StataEditor.CompletionsPlugin')

with open(os.path.join(DATA, 'test_config.json')) as f:
    config = json.load(f)
results = {}


class Tee(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, s):
        with open(CONSOLE_LOG, 'a', encoding='utf-8') as f:
            f.write(s)
        return self.stream.write(s)

    def flush(self):
        pass


sys.stdout = Tee(sys.stdout)
sys.stderr = Tee(sys.stderr)


def plugin_loaded():
    if config['mode'] == 'tests':
        sublime.set_timeout(lambda: wait_for_plugins(time.time()), 1000)


def record(name, func):
    try:
        results[name] = func()
    except Exception:
        results[name] = 'ERROR: ' + traceback.format_exc()


def wait_for_plugins(start):
    if not all(m in sys.modules for m in PLUGINS) and time.time() - start < 20:
        sublime.set_timeout(lambda: wait_for_plugins(start), 500)
        return

    results['python'] = '%d.%d' % sys.version_info[:2]
    results['plugins_loaded'] = [m for m in PLUGINS if m in sys.modules]
    record('pywin32', import_pywin32)
    view = sublime.active_window().open_file(os.path.join(FIXTURES, 'test.do'))
    wait_for_view(view)


def import_pywin32():
    import win32api
    import win32com.client
    return 'ok'


def wait_for_view(view):
    if view.is_loading():
        sublime.set_timeout(lambda: wait_for_view(view), 200)
        return

    # The plugin only completes where the scope is exactly "source.stata"
    end = view.size()
    view.sel().clear()
    view.sel().add(sublime.Region(end, end))
    record('function_completions', lambda: complete(view, 'FunctionCompletions'))
    if not config['stata']:
        finish()
        return

    view.run_command('stata_execute', {'Mode': 'do', 'Selection': 'default'})
    wait_for_stata(view, time.time())


def complete(view, listener):
    module = sys.modules['StataEditor.CompletionsPlugin']
    end = view.size()
    return getattr(module, listener)().on_query_completions(view, '', [end])


def wait_for_stata(view, start):
    output = os.path.join(FIXTURES, 'result.txt')
    if not os.path.exists(output) and time.time() - start < 60:
        sublime.set_timeout(lambda: wait_for_stata(view, start), 500)
        return

    # Give Stata a moment to finish writing
    time.sleep(1)
    record('stata_output', lambda: open(output).read().strip())
    record('variables', lambda: list(sublime.stata.VariableNameArray()))
    record('variable_completions', lambda: complete(view, 'VariableCompletions'))
    record('file_completions', lambda: complete(view, 'FileCompletions'))
    finish()


def finish():
    path = os.path.join(DATA, 'results.json')
    with open(path + '.tmp', 'w') as f:
        json.dump(results, f, indent=4)
    os.rename(path + '.tmp', path)
