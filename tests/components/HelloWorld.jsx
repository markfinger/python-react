var React = require('react');

// __DJANGO_WEBPACK_TRANSLATE_BUNDLE_TEST__

var HelloWorld = React.createClass({
    render: function() {
        return <span>Hello {this.props.name}</span>;
    }
});

module.exports = HelloWorld;