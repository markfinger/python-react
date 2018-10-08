Changelog
=========


### 4.3.0 (8/10/2018)

- Add option to pass a URL explicitly instead of reading from settings.
  ([jchen-eb](https://github.com/jchen-eb))
  https://github.com/markfinger/python-react/pull/88


### 4.2.1 (17/6/2018)

- Fix for a missing argument bug that could occur with rendering deactivated.


### 4.2.0 (17/6/2018)

- API for returning extra items returned by render server.
  ([Sassan Haradji](https://github.com/sassanh))
  https://github.com/markfinger/python-react/pull/87


### 4.1.1 (9/8/2017)

- Update timeout in render_server.py.
  ([Mike Plis](https://github.com/mplis))
  https://github.com/markfinger/python-react/pull/81


### 4.1.0 (1/3/2017)

- `render_component` now accepts a `timeout` keyword argument which is passed to `RenderServer.render`.
  ([Corey Burmeister](https://github.com/cburmeister))
  https://github.com/markfinger/python-react/pull/74


### 4.0.0 (28/2/2017)

- **Possibly breaking change** `RenderServer.render` now accepts a `timeout` keyword argument. There are some
  edge-cases where this may break down-stream code.
  ([Corey Burmeister](https://github.com/cburmeister))
  https://github.com/markfinger/python-react/pull/73
- Documentation updates regarding production environments. The key takeaway is to ensure that you are using
  the `NODE_ENV=production` environment variable so that React runs without debugging helpers which slow down
  rendering.
- Documentation updates regarding `RenderServer` API.


### 3.0.1 (6/4/2016)

- Documentation updates.


### 3.0.0 (6/4/2016)

- **Possibly breaking change** render_component now accepts a `request_headers` keyword argument.
  There are some edge-cases where this may break down-stream code. If you are overriding
  part of the render pipeline, you may need to ensure that you are using `**kwargs` to read and/or pass wildcard arguments.
  ([Ben Ilegbodu](https://github.com/benmvp))
  https://github.com/markfinger/python-react/pull/64
- [Documentation] Fix outdated link to server.js
  ([Jonathan Cox](https://github.com/geezhawk))
  https://github.com/markfinger/python-react/pull/60
- [Examples] missing babel-preset-es2015 in package.json in Tornado-example
  ([付雨帆](https://github.com/letfly))
  https://github.com/markfinger/python-react/pull/59
- [Examples] Added missing dependency on babel-preset-es2015
  ([Rune Juhl Jacobsen](https://github.com/runejuhl))
  https://github.com/markfinger/python-react/pull/56
- [Examples] Added es6 compiler plugin to .bablerc in basic_rendering
  ([Pringels](https://github.com/Pringels))
  https://github.com/markfinger/python-react/pull/55


### 2.0.0 (22/9/2015)

- **Breaking change** The base renderer's __init__  no longer accepts the RENDER_URL setting as an argument.
  The url is now resolved during calls, rather than initialisation.
- When used in companion with Django, settings will now be dynamically fetched rather than bound on
  initialisation. This enables a codebase to be more easily controlled from a test suite
- Updated docs regarding front-end integration


### 1.0.0 (13/7/2015)

- Removed the webpack integration. While it can be initially convenient, it tends to introduce more problems than
  it solves. The repo contains an example illustrating how to implement self-mounting components which provide
  similar functionality to the former webpack integration.
- Replaced the js-host dependency with an externally-managed render server.
- Added a `renderer` hook on `render_component`. Enabling you to override the default which assumes
  [render-react](https://github.com/markfinger/react-render)


### 0.13.1 (16/5/2015)

- Fixed a potential path issue in config files
- Replaced the webpack-service dependency with webpack-wrapper.


### 0.8.0 (26/1/2015)

- Boosting render performance by using a dedicated render server.
- Added a new setting, DJANGO_REACT['RENDERER'], which is a string denoting an import path to a
 callable object which returns a on object with a `render` method. By default it points to the new
 render server, 'django_react.render_server.ReactRenderServer'. The legacy renderer is useable by
 setting DJANGO_REACT['RENDERER'] = 'django_react.renderer.ReactRenderer'.


### 0.7.0 (2/1/2015)

- Changed `django_react.exceptions.ReactComponentMissingSourceAttribute` to `django_react.exceptions.ReactComponentMissingSource`
- `django_react.react.render` is now `django_react.render_component`
- Updated the django-webpack dependency to 2.0.0
- `django_react.models.ReactBundle` is now `django_react.ReactBundle`
- `django_react.models.ReactComponent` is now `django_react.ReactComponent`
- The Python<->JS bridge used to render components now relies on a `--serialized-props-file` argument, formerly it was `--serialized-props`.
- Switched the JSX loader to a fork which improves the debug information provided during error handling


### 0.6.0 (24/12/2014)

- The NODE_ENV environment setting is now controlled by the `DJANGO_REACT['DEBUG']` setting. Activating it will provides some improvements to the rendering performance.


### 0.5.0 (14/12/2014)

- Renamed `django_react.exceptions.PropSerialisationError` to `django_react.exceptions.PropSerializationError`.
- Rolled the bundling functionality out into a more easily overridable interface. You can now define a `bundle` attribute on `ReactComponent` inheritors which should be an extended `django_webpack.models.WebpackBundle`.
- Renamed the following attributes on `ReactComponent`:
  - `entry` is now `source`
  - `library` is now `variable`
- Renamed the `get_library` method on `ReactComponent` to `get_variable`
- Removed the following methods on `ReactComponent`:
  - `get_serialised_props_hash`
  - `get_component_id`
  - `get_react_variable`
  - `get_component_name`
  - `has_props`
- The render_* methods now use standard Django templates where possible.
- Removed the `render_to_string` and `render_to_static_markup` methods from `django_react.react`. In their place, use `django_react.react.render`.
- The react external can now be configured on a per-bundle basis, or globally by using the `DJANGO_REACT['REACT_EXTERNAL']` setting.
- Updated django-node and django-webpack dependencies to the latest.
- Added a test suite and harness.
- Added basic documentation.


### 0.4.0 (11/12/2014)

- Fixed a bug where errors caused during a component's prop serialization could silently fail.
- Excised the bundling tooling into a standalone app, `django_webpack`
- Renamed `SerialisationException` to `PropSerializationError`.
- Renamed `RenderException` to `RenderingError`.
- Renamed the `django_react.utils` module to `django_react.react`.
- `ReactComponent.render` is now `ReactComponent.render_to_string`
- `ReactComponent.render_static` is now `ReactComponent.render_to_static_markup`
- `ReactComponent.get_component_variable` is now `ReactComponent.get_library`.
- Moved the Webpack configuration into the ReactComponent class.


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
