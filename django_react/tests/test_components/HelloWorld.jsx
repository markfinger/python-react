var React = require('react');

var HelloWorld = React.createClass({
    render: function() {
        return <span>Hello {this.props.text}</span>;
    }
});

module.exports = HelloWorld;