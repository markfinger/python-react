var fs = require('fs');
var path = require('path');
var React = require('react');
var webpack = require('webpack');
var tmp = require('tmp');
var WebpackWatcher = require('webpack-watcher');

// Ensure that jsx files can be loaded
require('babel/register')({
	extensions: ['.jsx']
});

var pathToNodeModules = path.join(__dirname, 'node_modules');

var _watchedComponents = {};

var errorResponse = function(response, err) {
	console.error(new Error(err));
	response.status(500).send(err);
};

var renderComponent = function(component, props, toStaticMarkup, response) {
	var element = React.createElement(component, props);
	var output;
	var renderElement;
	if (toStaticMarkup) {
		renderElement = React.renderToStaticMarkup.bind(React);
	} else {
		renderElement = React.renderToString.bind(React);
	}
	try {
		output = renderElement(element);
	} catch(err) {
		errorResponse(response, err);
		return;
	}
	response.send(output);
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
					{test: /\.jsx$/, exclude: /node_modules/, loader: 'babel-loader'}
				]
			},
			resolveLoader: {root: pathToNodeModules}
		};
	}
	return watchedComponent.bundleConfig;
};

var getWatcher = function(pathToSource) {
	var watchedComponent = getWatchedComponent(pathToSource);
	if (!watchedComponent.watcher) {
		var compiler = webpack(getBundleConfig(pathToSource), function(err) {
			if (err) {
				console.error(new Error(err));
			}
		});

		var invalidateComponent = function() {
			watchedComponent.component = null;
		};

		watchedComponent.watcher = new WebpackWatcher(compiler, {
			onInvalid: invalidateComponent,
			onDone: invalidateComponent,
			onError: function(err) {
				if (err) {
					console.error(new Error(err));
				}
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
	watcher.onReady(function(stats) {
		if (stats.compilation.errors && stats.compilation.errors.length) {
			callback(stats.compilation.errors[0].message);
			return;
		}
		var watcherFileName = getWatcherFileName(pathToSource);
		//try {
			var content = watcher.readFileSync(watcherFileName);
		//} catch(e) {
		//	debugger
		//}
		var tempFile = tmp.fileSync();
		fs.writeFileSync(tempFile.name, content);
		try {
			var component = require(tempFile.name);
		} catch(err) {
			callback(err);
			return;
		}
		callback(null, component);
	});
};

var service = function(data, response) {
	var pathToSource = data.path_to_source;
	if (!pathToSource) {
		return errorResponse(response, 'No path_to_source option was provided');
	}

	var props;
	var serializedProps = data.serialized_props;
	if (serializedProps) {
		try {
			props = JSON.parse(serializedProps);
		} catch(e) {
			return errorResponse(response, e);
		}
	}

	var toStaticMarkup = data.to_static_markup;
	var watchComponentSource = data.watch_component_source;
	if (watchComponentSource) {
		// Initialise a watcher and render the component once
		// the component bundle has been generated
		watchComponent(pathToSource, function(err, component) {
			if (err) {
				return errorResponse(response, err);
			}
			renderComponent(component, props, toStaticMarkup, response);
		});
	} else {
		var component = require(pathToSource);
		renderComponent(component, props, toStaticMarkup, response);
	}
};

module.exports = service;