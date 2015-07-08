var http = require('http');
var express = require('express');
var bodyParser = require('body-parser');
var reactRender = require('react-render');

// Ensure support for JSX files
require('babel/register');

var ADDRESS = '127.0.0.1';
var PORT = 9009;

var app = express();
var server = http.Server(app);

app.use(bodyParser.json());

app.post('/render', function(req, res) {
	reactRender(req.body, function(err, markup) {
		res.json({
			error: err,
			markup: markup
		});
	});
});

server.listen(PORT, ADDRESS, function() {
	console.log('python-react test render server listening at http://' + ADDRESS + ':' + PORT);
});