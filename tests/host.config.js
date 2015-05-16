var reactRender = require('react-render');
var webpackWrapper = require('webpack-wrapper');

module.exports = {
	functions: {
		react: reactRender,
		webpack: webpackWrapper
	},
	// Force hosts to stop as soon as the python process exits
	disconnectTimeout: 0
};