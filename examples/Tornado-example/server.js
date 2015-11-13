var http = require('http');
var express = require('express');
var bodyParser = require('body-parser');
var reactRender = require('react-render');

// Ensure support for JSX files
require('babel-core/register');

var ADDRESS = '127.0.0.1';
var PORT = 9009;

var app = express();
var server = http.Server(app);

app.use(bodyParser.json());

app.get('/', function(req, res) {
	res.end('react render server');
});

app.post('/render', function(req, res) {
	reactRender(req.body, function(err, markup) {
		var error = null;
		if (err) {
			error = {
				type: err.constructor.name,
				message: err.message,
				stack: err.stack
			};
		}
		res.json({
			error: error,
			markup: markup
		});
	});
});

server.listen(PORT, ADDRESS, function() {
	console.log('react render server listening at http://' + ADDRESS + ':' + PORT);
});
