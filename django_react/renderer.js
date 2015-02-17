var fs = require('fs');
var React = require('react');

require('babel/register');

// `render-to` param options
var RENDER_TO_STATIC = 'static';
var RENDER_TO_STRING = 'string';

var render = function(req, res) {
	var pathToSource = req.query['path-to-source'];
	if (!pathToSource) {
		throw new Error('No path-to-source option was provided, ex: `?path-to-source=/path/to/file`');
	}
	pathToSource = decodeURIComponent(pathToSource);
	if (!fs.existsSync(pathToSource)) {
          throw new Error('The file specified by path-to-source, "' + pathToSource + '", cannot be found.');
        }
	var invalidateCache = req.query['invalidate-cache'] === 'true';
	if (invalidateCache) {
		delete require.cache[pathToSource];
	}
	var component = require(pathToSource);

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

	var renderTo = req.query['render-to'];
	if (!renderTo) {
		throw new Error('No render-to option was provided, ex: `?render-to=' + RENDER_TO_STATIC + '` or `?render-to=' + RENDER_TO_STRING + '`');
	}
	renderTo = decodeURIComponent(renderTo);

	var output;
	if (renderTo === RENDER_TO_STATIC) {
		output = React.renderToStaticMarkup(element);
	} else if (renderTo === RENDER_TO_STRING) {
		output = React.renderToString(element);
	} else {
		throw new Error('Unknown render-to option "' + renderTo + '", only "?render-to=' + RENDER_TO_STATIC + '" and "?render-to=' + RENDER_TO_STRING + '" are accepted');
	}

	res.send(output);
};

module.exports = render;
