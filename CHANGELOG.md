Changelog
=========

### 0.3.0 (3/12/2014)

- `django_react.exceptions.ReactComponentSourceFileNotFound` is now `django_react.exceptions.SourceFileNotFound`
- `django_react.exceptions.ReactComponentRenderToStringException` is now `django_react.exceptions.RenderException`
- `django_react.exceptions.ReactComponentBundleException` is now `django_react.exceptions.BundleException`
- `django_react.models.ReactComponent` now has additional methods: `generate_path_to_bundled_source`, `write_bundled_source_file`, `generate_bundled_source_file`, `get_rel_path_to_bundled_source`, and `get_url_to_bundled_source`.
- `django_react.utils.bundle` no longer accepts a `ReactComponent` as an argument, it now takes `entry` and `library`.
- `django_react.utils.render` no longer accepts a `ReactComponent` as an argument, it now takes `path_to_source`, `serialised_props`, and `to_static_markup`.
- `django_react/render.js` no longer accepts the `--path-to-component` argument, instead it takes `--path-to-source`.

### 0.2.0 (3/12/2014)

- Replaced the post-install step in setup.py with django-node's dependency and package resolver.

### 0.1.0 (2/12/2014)

- Initial release