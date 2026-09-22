"""Run StataEditor's tests in portable Sublime Text builds (Windows only)

For each build, Sublime Text is downloaded (once, into a cache) and unpacked afresh.
`tests/harness` checks from inside Sublime Text that the plugin loads on the right Python host,
that pywin32 imports and that completions work.

With `--stata`, it also runs `tests/fixtures/test.do` in Stata and checks the variable and file
completions. This needs a Stata license, so it is for local runs only; GitHub Actions runs w/o it.

    python tests/run_tests.py
    python tests/run_tests.py --stata
    python tests/run_tests.py --stata "C:/Program Files/Stata17/StataSE-64.exe"
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TESTS = REPO / 'tests'
WORK = Path(tempfile.gettempdir()) / 'StataEditor-tests'

# ST3, ST4 with the Python 3.8 host, ST4 with the Python 3.14 host
DEFAULT_BUILDS = [3211, 4200, 4213]
DEFAULT_STATA = 'C:/Program Files/Stata18/StataMP-64.exe'
PACKAGE_CONTROL_URL = ('https://github.com/wbond/package_control/releases/latest/download/'
                       'Package.Control.sublime-package')
PACKAGE_CONTROL_DONE = ('All specified packages up-to-date', 'Skipping automatic upgrade')
# The legacy "Pywin32" package, which ST3 users install by hand
PYWIN32_URL = 'https://github.com/SublimeText/Pywin32/archive/refs/heads/master.zip'
AUTO_VARIABLES = ['make', 'price', 'mpg', 'rep78', 'headroom', 'trunk', 'weight', 'length',
				  'turn', 'displacement', 'gear_ratio', 'foreign']


def sublime_url(build):
    if build < 4000:
        return f'https://download.sublimetext.com/Sublime%20Text%20Build%20{build}%20x64.zip'
    return f'https://download.sublimetext.com/sublime_text_build_{build}_x64.zip'


def download(url, dest):
    with urllib.request.urlopen(url) as response, open(dest, 'wb') as f:
        shutil.copyfileobj(response, f)


def cached_download(url, name):
    path = WORK / 'cache' / name
    if not path.exists():
        # Only on the first run, as it takes a while
        print(f'Downloading {name}', flush=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        download(url, path.with_suffix('.part'))
        path.with_suffix('.part').rename(path)
    return path


def package_files():
    """The working tree's files, as Package Control would ship them"""
    out = subprocess.run(['git', 'ls-files', '-co', '--exclude-standard'], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout
    return [f for f in out.splitlines()
            if not f.startswith(('tests/', '.github/')) and (REPO / f).exists()]


def set_up(build, args):
    """Unpack a fresh portable Sublime Text and install everything into it"""
    st_dir = WORK / f'st{build}'
    if st_dir.exists():
        shutil.rmtree(st_dir)
    zip_name = sublime_url(build).rsplit('/', 1)[1].replace('%20', ' ')
    with zipfile.ZipFile(cached_download(sublime_url(build), zip_name)) as z:
        z.extractall(st_dir)
    data = st_dir / 'Data'
    packages = data / 'Packages'

    (data / 'Installed Packages').mkdir(parents=True)
    download(PACKAGE_CONTROL_URL, data / 'Installed Packages' / 'Package Control.sublime-package')
    for f in package_files():
        dest = packages / 'StataEditor' / f
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / f, dest)
    if build < 4000:
        download(PYWIN32_URL, st_dir / 'Pywin32.zip')
        with zipfile.ZipFile(st_dir / 'Pywin32.zip') as z:
            z.extractall(st_dir)
        (st_dir / 'Pywin32-master').rename(packages / 'Pywin32')
    # The leading "0" makes the harness (alphabetically) load before StataEditor, so that its
    # console log catches StataEditor's import errors
    shutil.copytree(TESTS / 'harness', packages / '0StataEditorHarness')
    shutil.copytree(TESTS / 'fixtures', data / 'fixtures')

    user = packages / 'User'
    user.mkdir()
    write_json(user / 'Preferences.sublime-settings',
               {'update_check': False, 'hot_exit': False, 'remember_open_files': False})
    write_json(user / 'StataEditor.sublime-settings',
               {'stata_path': args.stata or '', 'stata_version': args.stata_version,
                'function_completions': True, 'waiting_time': 3})
    return st_dir


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=4))


def run_sublime(st_dir, done, timeout, what):
    """Start Sublime Text, wait until `done()` is true, then kill it"""
    proc = subprocess.Popen([str(st_dir / 'sublime_text.exe')])
    try:
        deadline = time.time() + timeout
        while not done():
            if time.time() > deadline:
                raise TimeoutError(f'Timed out after {timeout}s waiting for {what}')
            time.sleep(3)
    finally:
        # /T also kills the plugin hosts
        subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'], capture_output=True)
        time.sleep(3)


def read(path):
    return path.read_text(encoding='utf-8') if path.exists() else ''


def run_build(build, args):
    """Run the tests in one Sublime Text build and return a list of failures"""
    st_dir = set_up(build, args)
    data = st_dir / 'Data'
    console_log = data / 'console.log'
    config = data / 'test_config.json'

    if build >= 4000:
        # First start: Package Control installs the pywin32 library, which the plugin can only
        # import after a restart. The automatic upgrade runs after library installation and logs
        # one of these when it is done
        write_json(config, {'mode': 'bootstrap', 'stata': False})
        run_sublime(st_dir,
                    lambda: any(s in read(console_log) for s in PACKAGE_CONTROL_DONE),
                    180,
                    'Package Control to install libraries')
        console_log.rename(data / 'console-bootstrap.log')

    write_json(config, {'mode': 'tests', 'stata': bool(args.stata)})
    results_file = data / 'results.json'
    try:
        run_sublime(st_dir, results_file.exists, 180, 'the harness results')
    finally:
        kill_new_stata(args)
    results = json.loads(results_file.read_text())
    return check(build, results, data, args)


def check(build, r, data, args):
    failures = []

    def expect(ok, message):
        if not ok:
            failures.append(message)

    # The harness runs on the 3.8+ host in ST4, so seeing the plugins there means they did not
    # fall back to the 3.3 host
    expect(r['python'] == '3.3' if build < 4000 else r['python'] != '3.3',
           f'harness runs on Python {r["python"]}')
    expect(len(r['plugins_loaded']) == 2, f'plugins loaded: {r["plugins_loaded"]}')
    expect(r['pywin32'] == 'ok', f'pywin32 import: {r["pywin32"]}')
    expect(isinstance(r['function_completions'], list)
           and ['ceil\tFunction', 'ceil($1)$0'] in r['function_completions'],
           f'function completions: {r["function_completions"]}')
    if build < 4000:
        # `dependencies.json` asks for the pywin32 library on ST4 only
        expect(not (data / 'Lib' / 'python3.3' / 'win32com').exists(),
               'pywin32 library installed on ST3')
    # Python prints `SyntaxWarnings` only when it compiles a file, which is in the bootstrap start
    # on ST4. Tracebacks there are expected, as pywin32 is not installed yet
    errors = (plugin_errors(read(data / 'console-bootstrap.log'), tracebacks=False)
              + plugin_errors(read(data / 'console.log')))
    for error in errors:
        failures.append(f'console:\n{error}')

    if args.stata:
        expect(r['stata_output'] == 'ok N=74', f'Stata output: {r["stata_output"]}')
        expect(r['variables'] == AUTO_VARIABLES, f'variables: {r["variables"]}')
        expect(isinstance(r['variable_completions'], list)
               and ['make\tVariable', 'make'] in r['variable_completions'],
               f'variable completions: {r["variable_completions"]}')
        expect(isinstance(r['file_completions'], list)
               and ['./test.do\tfile', '"./test.do"'] in r['file_completions'],
               f'file completions: {r["file_completions"]}')
    return failures


def plugin_errors(console, tracebacks=True):
    """Tracebacks and warnings in the console that come from StataEditor"""
    marker = os.path.join('Packages', 'StataEditor', '')
    lines = console.splitlines()
    errors = []
    for i, line in enumerate(lines):
        if tracebacks and line.startswith('Traceback'):
            block = [line]
            for next_line in lines[i + 1:]:
                block.append(next_line)
                if not next_line.startswith(' '):
                    break
            if any(marker in b for b in block):
                errors.append('\n'.join(block))
        elif 'Warning' in line and marker in line:
            errors.append(line)
    return errors


def stata_pids(args):
    out = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {Path(args.stata).name}',
                          '/FO', 'CSV', '/NH'], capture_output=True, text=True, check=True)
    return {int(row.split('","')[1]) for row in out.stdout.splitlines() if row.startswith('"')}


def kill_new_stata(args):
    """Close the Stata that the test started"""
    if not args.stata:
        return
    for pid in stata_pids(args) - args.stata_pids_before:
        subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--builds', type=int, nargs='+', default=DEFAULT_BUILDS,
                        help=f'Sublime Text builds to test (default: {DEFAULT_BUILDS})')
    parser.add_argument('--stata', nargs='?', const=DEFAULT_STATA,
                        help=f'also test with Stata, at this path (default: {DEFAULT_STATA})')
    parser.add_argument('--stata-version', type=int, default=18,
                        help='Stata version, for the "stata_version" setting (default: 18)')
    args = parser.parse_args()

    if args.stata:
        if not Path(args.stata).is_file():
            sys.exit(f'Stata not found at {args.stata}')
        args.stata_pids_before = stata_pids(args)
        if args.stata_pids_before:
            # The plugin would attach to the running Stata and clear its data
            sys.exit('Stata is already running; close it before running the tests')

    all_failures = {}
    for build in args.builds:
        print(f'=== Sublime Text build {build} ===', flush=True)
        try:
            failures = run_build(build, args)
        except TimeoutError as e:
            failures = [str(e)]
        all_failures[build] = failures
        for f in failures:
            print(f'FAIL: {f}')
        if failures:
            print(f'--- console log ---\n{read(WORK / f"st{build}" / "Data" / "console.log")}')
        else:
            print('PASS')

    print('\n=== Summary ===')
    for build, failures in all_failures.items():
        print(f'{build}: {"FAIL" if failures else "PASS"}')
    sys.exit(1 if any(all_failures.values()) else 0)


if __name__ == '__main__':
    main()
