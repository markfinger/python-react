var React = require('react');
var HelloWorld = require('./HelloWorld.jsx');

var PerfTestComponent = React.createClass({
    render: function() {
        return <HelloWorld name={this.props.name} />;
    }
});

module.exports = PerfTestComponent;