var React = require('react');
var ReactWithAddons = require('react/addons');

var ReactAddonsComponent = React.createClass({
    render: function() {
		if (React.addons === undefined && ReactWithAddons.addons !== undefined) {
			return <span>Success</span>;
		}
        return <span>Fail</span>;
    }
});

module.exports = ReactAddonsComponent;