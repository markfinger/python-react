var fs = require('fs');
var path = require('path');
var React = require('react');
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
	this.component = null;

	if (this.watchSource) {
		this.watcherOutputFileName = tmp.tmpNameSync();
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
			path: path.dirname(this.watcherOutputFileName),
			filename: path.basename(this.watcherOutputFileName),
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
		}
	};
};

Component.prototype.invalidateComponent = function invalidateComponent() {
	this.component = null;
	this.factory = null;
};

Component.prototype.startWatcher = function startWatcher() {
	var compiler = webpack(this.watcherCompilerConfig, function(err) {
		if (err) {
			console.error(new Error(err));
		}
	});

	return new WebpackWatcher(compiler, {
		onInvalid: this.invalidateComponent.bind(this),
		onDone: this.invalidateComponent.bind(this),
		onError: function(err) {
			if (err) {
				console.error(new Error(err));
				this.invalidateComponent();
			}
		}.bind(this)
	});
};

Component.prototype.callPending = function callPending(err) {
	// Complete the pending requests
	var pending = this.pending;
	this.pending = [];
	pending.forEach(function(pending) {
		pending(err);
	});
};

Component.prototype.onWatchedComponentBuilt = function onWatchedComponentBuilt(callback) {
	// The component has already been built
	if (this.component) {
		return callback(null);
	}

	this.pending.push(callback);

	if (this.pending.length === 1) {
		this.watcher.onReady(function(stats) {
			if (stats.compilation.errors && stats.compilation.errors.length) {
				return callback(stats.compilation.errors[0].message);
			}

			var content = this.watcher.readFileSync(this.watcherOutputFileName);
			fs.writeFileSync(this.watcherOutputFileName, content);

			try {
				this.component = require(this.watcherOutputFileName);
			} catch(err) {
				this.callPending(err);
			}

			this.callPending(null);
		}.bind(this));
	}
};

Component.prototype.renderComponent = function renderComponent(options, callback) {
	if (!this.factory) {
		try {
			this.factory = React.createFactory(this.component);
		} catch(err) {
			return callback(err)
		}
	}

	var element = this.factory(options.props);

	var markup;
	try {
		if (options.toStaticMarkup) {
			markup = React.renderToStaticMarkup(element);
		} else {
			markup = React.renderToString(element);
		}
	} catch(err) {
		return callback(err);
	}

	callback(null, markup);
};

Component.prototype.render = function render(options, callback) {
	if (options.watchSource) {
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
	console.error(err);
	response.status(500).send(err.name + ': ' + err.message);
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
		component = new Component(options.pathToSource, options.watchSource);
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