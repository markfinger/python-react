var React = require('react');

// __WEBPACK_BUNDLE_TEST__

var HelloWorld = React.createClass({
    render: function() {
        return React.createElement("span", null, "Hello ", this.props.name);
    }
});

module.exports = HelloWorld;