var fs = require('fs');
var argv = require('yargs').argv;
var React = require('react');
var nodeJSX = require('node-jsx');

var pathToSource = argv.pathToSource;
if (!pathToSource) {
	throw new Error('No path to the source file was provided, ex: `--path-to-source /path/to/some/file.js`');
}

if (!fs.existsSync(pathToSource)) {
	throw new Error('Cannot find the source file "' + pathToSource + '"')
}

// Install support for requiring JSX files
nodeJSX.install();

var component = require(pathToSource);

var RENDER_TO_STATIC = 'static';
var RENDER_TO_STRING = 'string';

var renderTo = argv.renderTo;
if (!renderTo) {
	throw new Error('No render-to option was provided, ex: `--render-to ' + RENDER_TO_STATIC + '` or `--render-to ' + RENDER_TO_STRING + '`');
}
if (renderTo !== RENDER_TO_STATIC && renderTo !== RENDER_TO_STRING) {
	throw new Error('Unknown render-to option "' + renderTo + '", only "--render-to ' + RENDER_TO_STATIC + '" and "--render-to ' + RENDER_TO_STRING + '" are accepted');
}

var serializedPropsFile = argv.serializedPropsFile;
if (!serializedPropsFile) {
	throw new Error('No path to the serialized props file was provided, ex: `--serialised-props-file /path/to/some/file`');
}

var serializedProps = fs.readFileSync(serializedPropsFile);

var props = JSON.parse(serializedProps);

var element = React.createElement(component, props);

var output;
if (renderTo === RENDER_TO_STATIC) {
	output = React.renderToStaticMarkup(element);
} else if (renderTo === RENDER_TO_STRING) {
	output = React.renderToString(element);
}

// Push the rendered content to stdout
console.log(output);
