import React from 'react';

// During the build process webpack aliases this import to the desired component
import Component from '__react_mount_component__';

// During the build process webpack will replace these variable with
// the names passed from the python process
const props = __react_mount_props_variable__;
const container = document.getElementById(__react_mount_container__);

const element = React.createElement(Component, props);
React.render(element, container);