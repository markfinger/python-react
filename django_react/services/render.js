var fs = require('fs');
var path = require('path');
var resolve = require('resolve');
var webpack = require('webpack');
var tmp = require('tmp');
var WebpackWatcher = require('webpack-watcher');
var _ = require('lodash');

// Ensure that jsx files can be loaded
require('babel/register')({
	extensions: ['.jsx']
});

var pathToNodeModules = path.join(__dirname, 'node_modules');
var components = [];

var Component = function Component(pathToSource, watchSource) {
	this.pathToSource = pathToSource;
	this.watchSource = watchSource;
	this.pathToReact = resolve.sync('react', {
		basedir: path.dirname(pathToSource)
	});
	this.component = null;
	if (this.watchSource) {
		// The in-memory file that the watcher is outputting the component to
		this.pathToWatcherFileInMemory = tmp.tmpNameSync();
		// The file name that we write the component to when requiring it
		this.pathToWatcherFileInFS = this.pathToWatcherFileInMemory;
		this.watcherCompilerConfig = this.getWatcherCompilerConfig();
		this.watcher = this.startWatcher();
		this.pending = [];
	}
};

Component.prototype.getWatcherCompilerConfig = function getWatcherCompilerConfig() {
	return {
		context: path.dirname(this.pathToSource),
		entry: './' + path.basename(this.pathToSource),
		output: {
			path: path.dirname(this.pathToWatcherFileInMemory),
			filename: path.basename(this.pathToWatcherFileInMemory),
			libraryTarget: 'commonjs2'
		},
		target: 'node',
		module: {
			loaders: [
				// JSX + ES6/7 support
				{
					test: /\.jsx$/,
					exclude: /node_modules/,
					loader: 'babel-loader'
				}
			]
		},
		resolveLoader: {
			root: pathToNodeModules
		},
		devtool: 'eval'
	};
};

Component.prototype.invalidateComponent = function invalidateComponent() {
	if (this.component) {
		console.log('Invalidated watched component');
		this.component = null;
		// Ensure that the bundled component is written to a new file
		// so that we can circumvent node's module cache
		this.pathToWatcherFileInFS = tmp.tmpNameSync();
	}
};

Component.prototype.startWatcher = function startWatcher() {
	console.log('Starting component watcher');

	var compiler = webpack(this.watcherCompilerConfig, function(err) {
		if (err) {
			console.error(new Error(err));
		}
	});

	return new WebpackWatcher(compiler, {
		onInvalid: function() {
			console.log('Component watcher triggered onInvalid');
			this.invalidateComponent();
		}.bind(this),
		onDone: function() {
			console.log('Component watcher triggered onDone');
			this.invalidateComponent();
		}.bind(this),
		onError: function(err) {
			console.log('Component watcher triggered onError');
			if (err) {
				console.error(new Error(err));
				this.invalidateComponent();
			}
		}.bind(this)
	});
};

Component.prototype.callPending = function callPending(err) {
	// Complete the pending requests
	console.log('Sending pending requests for watched component');
	var pending = this.pending;
	this.pending = [];
	pending.forEach(function(pending) {
		pending(err);
	});
};

Component.prototype.onWatchedComponentBuilt = function onWatchedComponentBuilt(callback) {
	// The component has already been built
	console.log('Watched component already built');
	if (this.component) {
		return callback(null);
	}

	console.log('Added pending callback for watched component');
	this.pending.push(callback);

	if (this.pending.length === 1) {
		console.log('Waiting for watcher to build component');
		this.watcher.onReady(function(stats) {
			console.log('Finished waiting for watcher to build component');

			if (stats.compilation.errors && stats.compilation.errors.length) {
				return callback(stats.compilation.errors[0].message);
			}

			console.log('Reading watched component from memory');

			var content = this.watcher.readFileSync(this.pathToWatcherFileInMemory);

			console.log('Writing watched component to file system');

			try {
				fs.writeFileSync(this.pathToWatcherFileInFS, content);
			} catch(err) {
				return this.callPending(err);
			}

			console.log('Requiring watched component');

			try {
				this.component = require(this.pathToWatcherFileInFS);
			} catch(err) {
				return this.callPending(err);
			}

			this.callPending(null);
		}.bind(this));
	}
};

Component.prototype.renderWithResolvedReact = function(options) {
	var React = require(this.pathToReact);
	var element = React.createElement(this.component, options.props);
	if (options.toStaticMarkup) {
		console.log('Rendering component to static markup');
		return React.renderToStaticMarkup(element);
	}
	console.log('Rendering component to a string');
	return React.renderToString(element);
};

Component.prototype.renderComponent = function renderComponent(options, callback) {
	console.log('Rendering component');
	try {
		var markup = this.renderWithResolvedReact(options);
	} catch(err) {
		return callback(err);
	}
	console.log('Rendered component');
	callback(null, markup);
};

Component.prototype.render = function render(options, callback) {
	if (options.watchSource) {
		console.log('watching component');
		// Render the component once the watched component has been built
		return this.onWatchedComponentBuilt(function(err) {
			if (err) {
				return callback(err);
			}
			this.renderComponent(options, callback);
		}.bind(this));
	}

	try {
		this.component = require(options.pathToSource);
	} catch(err) {
		return callback(err);
	}

	this.renderComponent(options, callback);
};

var onError = function onError(response, err) {
	if (!(err instanceof Error)) {
		err = new Error(err);
	}
	console.error(err.stack);
	response.status(500).send(err.stack);
};

var service = function service(data, response) {
	var options = {
		pathToSource: data.path_to_source,
		serializedProps: data.serialized_props,
		props: null,
		toStaticMarkup: data.to_static_markup,
		watchSource: data.watch_source
	};

	if (!options.pathToSource) {
		return onError(response, 'No path_to_source option was provided');
	}

	if (options.serializedProps) {
		try {
			options.props = JSON.parse(options.serializedProps);
		} catch(e) {
			return onError(response, e);
		}
	}

	var component = _.find(components, {
		pathToSource: options.pathToSource,
		watchSource: options.watchSource
	});

	if (!component) {
		console.log('Creating new Component instance', options.pathToSource, options.watchSource);
		try {
			component = new Component(options.pathToSource, options.watchSource);
		} catch(err) {
			return onError(response, err)
		}
		components.push(component);
	}

	component.render(options, function(err, output) {
		if (err) {
			return onError(response, err);
		}
		response.send(output);
	});
};

module.exports = service;