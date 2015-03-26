var resolve = require('resolve');
var express = require('express');
var bodyParser = require('body-parser');
var argv = require('yargs').argv;
require('node-jsx').install({extension: '.jsx'});

var app = express();
app.use(bodyParser.json());


var components = {};

var Component = function Component(pathToSource) {
	this.pathToSource = pathToSource;
	this.pathToReact = resolve.sync('react', {
		basedir: path.dirname(pathToSource)
	});
	this.component = null;
};

Component.prototype.render = function render(props, toStaticMarkup, callback) {
	console.log('Reacting...');
	try {
    if (this.component == null) {
      this.component = require(this.pathToSource);
    }
	  var React = require(this.pathToReact);
	  var element = React.createElement(this.component, props);
    console.log('loaded');
    if (toStaticMarkup) {
      callback(null, React.renderToStaticMarkup(element));
    } else {
      callback(null, React.renderToString(element));
    }
	} catch(err) {
		return callback(err);
	}
};

var onError = function onError(response, err) {
	if (!(err instanceof Error)) {
		err = new Error(err);
	}
	console.error(err.stack);
	response.status(500).send(err.stack);
};

app.post('/render', function service(request, response) {
  var toStaticMarkup = request.body.to_static_markup || false;
  var pathToSource = request.body.path_to_source;
  var props = request.body.props;

	if (!pathToSource) {
		return onError(response, 'No path_to_source option was provided');
	}

  var component = null;
	if (pathToSource in components) {
    component = components[pathToSource];
  } else {
		console.log('Loading new component', pathToSource);
		try {
			component = new Component(pathToSource);
		} catch(err) {
			return onError(response, err)
		}
		components[pathToSource] = component;
	}

	component.render(props, toStaticMarkup, function(err, output) {
		if (err) {
			return onError(response, err);
		}
    console.log('Done');
		response.send(output);
	});
});

var server = app.listen(argv.port || 63578, 'localhost', function() {
	var host = server.address().address;
	var port = server.address().port;

	console.log('Started server at http://%s:%s', host, port);
});

module.exports = app;
