var http = require('http');
var fs = require('fs');
var argv = require('yargs').argv;
var express = require('express');
var React = require('react');
var nodeJSX = require('node-jsx');

// Support requiring of JSX files
nodeJSX.install();

// `render-to` param options
var RENDER_TO_STATIC = 'static';
var RENDER_TO_STRING = 'string';

var app = express();

var address = argv.address;
if (address === undefined) {
	throw new Error('No address was provided, ex: `--address 127.0.0.1`');
}

var port = argv.port;
if (port === undefined) {
	throw new Error('No port was provided, ex: `--port 0`');
}

var server = app.listen(port, address, function() {
	console.log('Started django-react render server');
	var output = JSON.stringify(server.address());
	console.log(output);
});

app.get('/', function(req, res) {
	res.send('django-react render server');
});

app.get('/render', function(req, res) {
	var pathToSource = req.query['path-to-source'];
	if (!pathToSource) {
		throw new Error('No path-to-source option was provided, ex: `?path-to-source=/path/to/file`');
	}
	pathToSource = decodeURIComponent(pathToSource);
	if (!fs.existsSync(pathToSource)) {
		throw new Error('The file specified by path-to-source, "' + pathToSource + '", cannot be found.');
	}
	var component = require(pathToSource);

	var renderTo = req.query['render-to'];
	if (!renderTo) {
		throw new Error('No render-to option was provided, ex: `?render-to=' + RENDER_TO_STATIC + '` or `?render-to=' + RENDER_TO_STRING + '`');
	}
	renderTo = decodeURIComponent(renderTo);
	if (renderTo !== RENDER_TO_STATIC && renderTo !== RENDER_TO_STRING) {
		throw new Error('Unknown render-to option "' + renderTo + '", only "?render-to=' + RENDER_TO_STATIC + '" and "?render-to=' + RENDER_TO_STRING + '" are accepted');
	}

	var props = undefined;
	var pathToSerializedProps = req.query['path-to-serialized-props'];
	if (pathToSerializedProps) {
		pathToSerializedProps = decodeURIComponent(pathToSerializedProps);
		if (!fs.existsSync(pathToSerializedProps)) {
			throw new Error('The file specified by path-to-serialized-props, "' + pathToSerializedProps + '", cannot be found.');
		}
		var serializedProps = fs.readFileSync(pathToSerializedProps);
		props = JSON.parse(serializedProps);
	}

	var element = React.createElement(component, props);

	var output;
	if (renderTo === RENDER_TO_STATIC) {
		output = React.renderToStaticMarkup(element);
	} else if (renderTo === RENDER_TO_STRING) {
		output = React.renderToString(element);
	}

	res.send(output);
});