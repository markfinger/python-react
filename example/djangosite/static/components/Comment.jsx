import React from 'react';
import marked from 'marked';

export default React.createClass({
	render() {
		var rawMarkup = marked(this.props.text);
		return (
			<div>
				<h3>
          			{this.props.author}
				</h3>
				<span dangerouslySetInnerHTML={{__html: rawMarkup}} />
			</div>
		);
	}
});