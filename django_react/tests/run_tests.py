if __name__ == '__main__':
    import os
    import sys
    import subprocess
    path_to_python = sys.executable
    path_to_file = os.path.abspath(os.path.dirname(__file__))

    test_files = (
        'functional/run_tests.py',
        'performance/run_tests.py',
    )

    print('')
    for test_file in test_files:
        popen = subprocess.Popen(
            (path_to_python, os.path.join(path_to_file, test_file),)
        )
        popen.wait()
        print('')

    sys.exit()