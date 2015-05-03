var reactRender = require('react-render');
var webpackService = require('webpack-service');

module.exports = {
	functions: {
		react: reactRender,
		webpack: webpackService
	},
	// Force hosts to stop as soon as the python process exits
	disconnectTimeout: 0
};