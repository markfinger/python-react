var reactRender = require('react-render');
var webpackService = require('webpack-service');

module.exports = {
	functions: {
		react: reactRender,
		webpack: webpackService
	}
};