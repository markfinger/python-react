var React = require('react');

var HelloWorld = React.createClass({
    render: function() {
        return <span>Hello {this.props.name}</span>;
    }
});

module.exports = HelloWorld;