import os
import atexit
import subprocess

process = subprocess.Popen(
    args=('node', os.path.join(os.path.dirname(__file__), '..', 'example', 'server.js'),),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

# Ensure the process is killed on exit
atexit.register(lambda _process: _process.kill(), process)

output = process.stdout.readline().decode('utf-8')

if output.strip() == '':
    output += process.stdout.readline().decode('utf-8')

if 'render server' not in output:
    raise Exception('Unexpected output: "{}"'.format(output))
