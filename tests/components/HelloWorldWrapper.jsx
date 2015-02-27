var React = require('react');
var HelloWorld = require('./HelloWorld.jsx');

var HelloWorldWrapper = React.createClass({
    render: function() {
        var numbers = this.props.numbers.map(function(number) {
			return number * 10;
		}).join(', ');
		return (
			<div>
				<HelloWorld text={this.props.text} />
				<span>{numbers}</span>
			</div>
		);
    }
});

module.exports = HelloWorldWrapper;
