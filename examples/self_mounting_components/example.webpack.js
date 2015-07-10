var path = require('path');
var webpack = require('webpack');
var autoprefixer = require('autoprefixer-core');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = function(opts) {
	var config = {
		context: __dirname,
		entry: './mount',
		output: {
			filename: '[name]-[hash].js',
			pathinfo: opts.context.DEBUG
		},
		module: {
			loaders: [
				{
					test: /\.jsx?$/,
					exclude: /(node_modules|bower_components)/,
					loader: (opts.hmr ? 'react-hot-loader!': '') + 'babel-loader'
				},
				{
					test: /\.css$/,
					loader: opts.hmr ?
						'style!css-loader?sourceMap!postcss-loader' :
						ExtractTextPlugin.extract('style', 'css-loader?sourceMap!postcss-loader')
				},
				{
					test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
					loader: 'url-loader?limit=10000&mimetype=application/font-woff'
				},
				{
					test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
					loader: 'file-loader'
				}
			]
		},
		postcss: [autoprefixer],
		resolve: {
			alias: {
				__react_mount_component__: opts.context.component
			}
		},
		plugins: [
			// Define the variables in `./mount.js` that webpack will replace with data from python
			new webpack.DefinePlugin({
				__react_mount_props_variable__: opts.context.props_var,
				__react_mount_container__: JSON.stringify(opts.context.container)
			}),
			new webpack.optimize.OccurrenceOrderPlugin(),
			new webpack.NoErrorsPlugin(),
			new webpack.DefinePlugin({
				'process.env': {
					NODE_ENV: JSON.stringify(
						opts.context.DEBUG ? 'development' : 'production'
					)
				}
			})
		],
		devtool: opts.context.DEBUG ? 'eval-source-map' : 'source-map'
	};

	if (!opts.hmr) {
		// Move css assets into separate files
		config.plugins.push(new ExtractTextPlugin('[name]-[contenthash].css'));
	}

	if (!opts.context.DEBUG) {
		// Remove duplicates and activate compression
		config.plugins.push(
			new webpack.optimize.DedupePlugin(),
			new webpack.optimize.UglifyJsPlugin()
		);
	}

	return config;
};