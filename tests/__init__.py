import os
import atexit
import subprocess

process = subprocess.Popen(
    args=('node', os.path.join(os.path.dirname(__file__), 'test_server.js'),),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

# Ensure the process is killed on exit
atexit.register(lambda _process: _process.kill(), process)

def read_line():
    return process.stdout.readline().decode('utf-8')

output = read_line()
if output.strip() == '':
    output += read_line()

if 'React render server' not in output:
    if 'module.js' in output:
        line = read_line()
        while line:
            output += line + os.linesep
            line = read_line()
    raise Exception('Unexpected output from render server subprocess...' + os.linesep + os.linesep + output)
