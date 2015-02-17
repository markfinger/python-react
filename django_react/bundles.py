import os
from django_webpack import WebpackBundle


class ReactBundle(WebpackBundle):
    # Use the JSX loader for files ending in a 'jsx' extension.
    loaders = (
        {'loader': 'babel', 'test': '.jsx$'},
    )
    # Ensure that Webpack's loader resolver will look in Django React's
    # node_modules directory to find the JSX loader
    paths_to_loaders = (os.path.join(os.path.dirname(__file__), 'node_modules'),)
