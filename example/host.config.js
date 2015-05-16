var reactRender = require('react-render');
var webpackWrapper = require('webpack-wrapper');

module.exports = {
	functions: {
		react: reactRender,
		webpack: webpackWrapper
	}
};