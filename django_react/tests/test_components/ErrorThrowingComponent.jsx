var React = require('react');

var ErrorThrowingComponent = React.createClass({
    render: function() {
        throw Error();
    }
});

module.exports = ErrorThrowingComponent;