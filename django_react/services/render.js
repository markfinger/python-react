var fs = require('fs');
var path = require('path');
var React = require('react');
var webpack = require('webpack');
//var webpackDevMiddleware = require('webpack-dev-middleware');
var temp = require('temp');

// `render_to` param options
var RENDER_TO_STATIC = 'STATIC';
var RENDER_TO_STRING = 'STRING';

var errorResponse = function(response, error) {
	console.error(new Error(error));
	response.status(500).send(error);
};

// TODO: try loading a JSX/ES6 file rather than assuming babel has not already been installed
var isJSXSupported = false;
var ensureJSXSupport = function() {
	// TODO: is there a way to restrict the register to .jsx?
	if (!isJSXSupported) {
		require('babel/register');
		isJSXSupported = true;
	}
};

var renderComponent = function(component, props, renderTo, response) {
	var element = React.createElement(component, props);
	if (renderTo === RENDER_TO_STATIC) {
		response.send(React.renderToStaticMarkup(element));
	} else {
		response.send(React.renderToString(element));
	}
};

var getBundleOutput = function() {
	return temp.path({suffix: '.js'});
};

var generateBundleConfig = function(pathToSource, pathToOutput) {
	return {
		context: path.dirname(pathToSource),
		entry: './' + path.basename(pathToSource),
		output: {
			path: path.dirname(pathToOutput),
			filename: path.basename(pathToOutput),
			libraryTarget: 'commonjs2'
		},
		target: 'node',
		module: {
			loaders: [
				{test: /\.jsx$/, exclude: /node_modules/, loader: 'babel'}
			]
		},
		resolve: {
			root: path.join(__dirname, '..', 'node_modules')
		}
	};
};

var bundleRequire = function(pathToSource, response, callback) {
	// Circumvents the require module cache by bundling a module
	// then reading it in and passing it to `callback`

	//webpackDevMiddleware

	var pathToOutput = getBundleOutput();
	var config = generateBundleConfig(pathToSource, pathToOutput);

	webpack(config, function(error, stats) {
		if (error) {
			return errorResponse(response, error);
		}

		if (stats.hasErrors()) {
			return errorResponse(response, stats.toJson().errors);
		}

		if (stats.hasWarnings()) {
			console.warn(stats.toJson().warnings);
		}

		if (pathToOutput in require.cache) {
			delete require.cache[pathToOutput];
		}

		var requireFailed = false;
		try {
			var requiredModule = require(pathToOutput);
		} catch(e) {
			requireFailed = true;
			var message = (
				'Failed to `require` the bundle generated from ' +
				pathToSource + '. Error: ' + e.message
			);
			errorResponse(response, message);
		}

		// Remove the generated bundle
		fs.unlink(pathToOutput, function(error) {
			if (error) {
				console.error(error);
			}
		});

		if (!requireFailed) {
			callback(requiredModule)
		}
	});
};

var service = function(request, response) {
	var pathToSource = request.query.path_to_source;
	if (!pathToSource) {
		return errorResponse(response, 'No path_to_source option was provided');
	}

	var props;
	var serializedProps = request.query.serialized_props;
	if (serializedProps) {
		try {
			props = JSON.parse(serializedProps);
		} catch(e) {
			return errorResponse(response, e);
		}
	}

	var renderTo = request.query.render_to;
	if (!renderTo) {
		return errorResponse(
			response,
			'No render-to option was provided, must be "' + RENDER_TO_STATIC + '" or "' + RENDER_TO_STRING + '"'
		);
	} else if (renderTo !== RENDER_TO_STATIC && renderTo !== RENDER_TO_STRING) {
		return errorResponse(
			response,
			'Unknown render_to option "' + renderTo + '", must be "' + RENDER_TO_STATIC + '" or "' + RENDER_TO_STRING + '"'
		);
	}

	var cacheComponentSource = request.query.cache_component_source === 'True';

	if (cacheComponentSource) {
		ensureJSXSupport();
		renderComponent(require(pathToSource), props, renderTo, response);
	} else {
		bundleRequire(pathToSource, response, function(component) {
			renderComponent(component, props, renderTo, response);
		});
	}
};

module.exports = service;