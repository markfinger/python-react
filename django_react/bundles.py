import os
from django_webpack import WebpackBundle
from .settings import REACT_EXTERNAL


class ReactBundle(WebpackBundle):
    # Use the JSX loader for files ending in a 'jsx' extension.
    loaders = (
        {'loader': 'jsx', 'test': '.jsx$'},
    )
    # Ensure that Webpack's loader resolver will look in Django React's
    # node_modules directory to find the JSX loader
    paths_to_loaders = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'node_modules')),)
    # Rather than bundling React, we rely on a browser global. This improves
    # the speed of generating bundles and allows for multiple components to be
    # injected into the page without duplicating React's source code.
    externals = {
        'react': REACT_EXTERNAL,
        'react/addons': REACT_EXTERNAL,
    }