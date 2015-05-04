import sys

if 'nosetests' in sys.argv[0]:
    # Configure js-host and webpack before any tests are run
    import js_host.conf
    import webpack.conf
    from .settings import JS_HOST, WEBPACK
    js_host.conf.settings.configure(**JS_HOST)
    webpack.conf.settings.configure(**WEBPACK)
