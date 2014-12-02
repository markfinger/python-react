var fs = require('fs');
var path = require('path');
var argv = require('yargs').argv;
var webpack = require('webpack');

var entry = argv.entry;
if (!entry) {
	throw new Error('No entry point specified for the bundle, ex: `--entry=/path/to/some/file.js`');
}

if (!fs.existsSync(entry)) {
    throw new Error('Cannot find entry file "' + entry + '"');
}

var output = argv.output;
if (!output) {
	throw new Error('No output path specified for the bundle, ex: `--output=/path/to/some/file.js`');
}

var library = argv.library;
if (!library) {
	throw new Error('No library name specified for the bundle, ex: `--library=someVariable`');
}


webpack({
    entry: entry,
    output: {
        filename: output,
		library: library
    },
	// TODO: make this extensible
	externals: {
		// Rather than bundling React, we use the browser's global
		react: 'window.React',
		'react/addons': 'window.React'
	},
	module: {
		loaders: [
			// Pass *.jsx files through the jsx-loader transform
			{ test: /\.jsx$/, loader: 'jsx' }
		]
	},
	resolveLoader: {
		// Instruct webpack to use our node_modules for resolving loaders
		root: [path.join(__dirname, 'node_modules')]
	},
	// TODO: make this configurable
	devtool: 'eval-source-map'
	// TODO: make this configurable, and try to see if we can resolve the file where the error is triggered
//	bail: true
}, function(err) {
    if (err) {
		throw new Error(err);
	}
});