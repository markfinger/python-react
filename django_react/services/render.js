var fs = require('fs');
var React = require('react');

require('babel/register');

// `render-to` param options
var RENDER_TO_STATIC = 'STATIC';
var RENDER_TO_STRING = 'STRING';

var render = function(request, response) {
	var pathToSource = request.query.path_to_source;
	if (!pathToSource) {
		throw new Error('No path_to_source option was provided');
	}

	var invalidateCache = request.query.invalidate_cache === 'True';
	if (invalidateCache) {
		delete require.cache[pathToSource];
	}

	var component = require(pathToSource);

	var props;
	var serializedProps = request.query.serialized_props;
	if (serializedProps) {
		props = JSON.parse(serializedProps);
	}

	var renderTo = request.query.render_to;
	if (!renderTo) {
		throw new Error('No render-to option was provided, must be "' + RENDER_TO_STATIC + '" or "' + RENDER_TO_STRING + '"');
	} else if (renderTo !== RENDER_TO_STATIC && renderTo !== RENDER_TO_STRING) {
		throw new Error('Unknown render_to option "' + renderTo + '", must be "' + RENDER_TO_STATIC + '" or "' + RENDER_TO_STRING + '"');
	}

	var element = React.createElement(component, props);

	if (renderTo === RENDER_TO_STATIC) {
		response.send(React.renderToStaticMarkup(element));
	} else {
		response.send(React.renderToString(element));
	}
};

module.exports = render;
