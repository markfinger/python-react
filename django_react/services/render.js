var fs = require('fs');
var path = require('path');
var React = require('react');
var webpack = require('webpack');
var tmp = require('tmp');
var WebpackWatcher = require('./webpack-watcher');

// `render_to` param options
var RENDER_TO_STATIC = 'STATIC';
var RENDER_TO_STRING = 'STRING';

// TODO: try loading a JSX/ES6 file rather than assuming babel has not already been installed
var isJSXSupported = false;
var _watchedComponents = {};

var errorResponse = function(response, err) {
	console.error(new Error(err));
	response.status(500).send(err);
};

var renderComponent = function(component, props, renderTo, response) {
	var element = React.createElement(component, props);
	if (renderTo === RENDER_TO_STATIC) {
		response.send(React.renderToStaticMarkup(element));
	} else {
		response.send(React.renderToString(element));
	}
};

var ensureJSXSupport = function() {
	// TODO: is there a way to restrict babel by white-listing jsx files?
	if (!isJSXSupported) {
		require('babel/register');
		isJSXSupported = true;
	}
};

var getWatchedComponent = function(pathToSource) {
	if (_watchedComponents[pathToSource] === undefined) {
		_watchedComponents[pathToSource] = {
			bundleConfig: null,
			watcherFileName: null,
			watcher: null,
			component: null
		};
	}
	return _watchedComponents[pathToSource];
};

var getWatcherFileName = function(pathToSource) {
	var watchedComponent = getWatchedComponent(pathToSource);
	if (!watchedComponent.watcherFileName) {
		watchedComponent.watcherFileName = tmp.tmpNameSync();
	}
	return watchedComponent.watcherFileName;
};

var getBundleConfig = function(pathToSource) {
	var watchedComponent = getWatchedComponent(pathToSource);
	if (!watchedComponent.bundleConfig) {
		var watcherFileName = getWatcherFileName(pathToSource);
		watchedComponent.bundleConfig = {
			context: path.dirname(pathToSource),
			entry: './' + path.basename(pathToSource),
			output: {
				path: path.dirname(watcherFileName),
				filename: path.basename(watcherFileName),
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
	}
	return watchedComponent.bundleConfig;
};

var getWatcher = function(pathToSource) {
	var watchedComponent = getWatchedComponent(pathToSource);
	if (!watchedComponent.watcher) {
		var compiler = webpack(getBundleConfig(pathToSource));
		watchedComponent.watcher = new WebpackWatcher(compiler, {
			onInvalid: function() {
				console.log('onInvalid called');
				watchedComponent.component = null;
			},
			onDone: function() {
				console.log('onDone called');
				watchedComponent.component = null;
			},
			onError: function(error) {
				console.log('onError called');
			}
		});
	}
	return watchedComponent.watcher;
};

var watchComponent = function(pathToSource, callback) {
	var watchedComponent = getWatchedComponent(pathToSource);

	// The component has already been generated
	if (watchedComponent.component) {
		return callback(watchedComponent.component);
	}

	// Wait until the component has been generated
	var watcher = getWatcher(pathToSource);
	watcher.onReady(function() {
		var watcherFileName = getWatcherFileName(pathToSource);
		var tempFile = tmp.fileSync();
		var content = watcher.readFileSync(watcherFileName);
		fs.writeFileSync(tempFile.name, content);
		try {
			var component = require(tempFile.name);
		} catch(err) {
			callback(err);
			return
		}
		callback(null, component);
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

	var watchComponentSource = request.query.watch_component_source === 'True';

	if (watchComponentSource) {
		// Initialise a watcher and render the component once
		// the component bundle has been generated
		watchComponent(pathToSource, function(err, component) {
			if (err) {
				return errorResponse(response, err);
			}
			renderComponent(component, props, renderTo, response);
		});
	} else {
		ensureJSXSupport();
		var component = require(pathToSource);
		renderComponent(component, props, renderTo, response);
	}
};

module.exports = service;