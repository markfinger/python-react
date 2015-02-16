var React = require('react');

var HelloWorld = React.createClass({displayName: 'HelloWorld',
    render: function() {
        return React.createElement("span", null, "Hello ", this.props.text);
    }
});

module.exports = HelloWorld;