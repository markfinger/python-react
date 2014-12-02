var fs = require('fs');
var path = require('path');
var argv = require('yargs').argv;
var React = require('react');
var nodeJSX = require('node-jsx');

var pathToComponent = argv.pathToComponent;
if (!pathToComponent) {
	throw new Error('No path to the component specified, ex: `--path-to-component /path/to/some/component.js`');
}

if (!fs.existsSync(pathToComponent)) {
    throw new Error('Cannot find file "' + pathToComponent + '"')
}

// Install support for requiring JSX files
nodeJSX.install();

var component = require(pathToComponent);

var RENDER_TO_STATIC = 'static';
var RENDER_TO_STRING = 'string';

var renderTo = argv.renderTo;
if (!renderTo) {
	throw new Error('No render to option provided, ex: `--render-to ' + RENDER_TO_STATIC + '` or `--render-to ' + RENDER_TO_STRING + '`');
}
if (renderTo !== RENDER_TO_STATIC && renderTo !== RENDER_TO_STRING) {
	throw new Error('Unknown render to option "' + renderTo + '", only "--render-to ' + RENDER_TO_STATIC + '" and "--render-to ' + RENDER_TO_STRING + '" are accepted');
}

var serialisedProps = argv.serialisedProps;
if (!serialisedProps) {
	throw new Error('No path to props file provided');
}

serialisedProps = fs.readFileSync(serialisedProps);

var props = JSON.parse(serialisedProps);

var element = React.createElement(component, props);

var output;
if (renderTo === RENDER_TO_STATIC) {
	output = React.renderToStaticMarkup(element);
} else if (renderTo === RENDER_TO_STRING) {
	output = React.renderToString(element);
}

// Push the output to stdout
console.log(output);