MOUNT_JS = \
"""
if (typeof React === 'undefined') throw new Error('Cannot find `React` global variable. Have you added a script element to this page which points to React?');
if (typeof {var} === 'undefined') throw new Error('Cannot find component variable `{var}`');
(function(React, component, containerId) {{
  var props = {props};
  var element = React.createElement(component, props);
  var container = document.getElementById(containerId);
  if (!container) throw new Error('Cannot find the container element `#{container_id}` for component `{var}`');
  React.render(element, container);
}})(React, {var}, '{container_id}');
"""