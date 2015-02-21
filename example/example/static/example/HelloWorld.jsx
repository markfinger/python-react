var React = require('react');

if (typeof window !== 'undefined') { window.React = React; }

var HelloWorld = React.createClass({
    render: function() {
        return <span>Hello, {this.props.name}!</span>;
    }
});

module.exports = HelloWorld;