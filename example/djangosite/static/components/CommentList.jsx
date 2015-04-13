import React from 'react';
import Comment from './Comment.jsx';

export default React.createClass({
	render() {
		if (!this.props.comments.length) {
			return null;
		}
		var commentNodes = this.props.comments.map((comment, index) => {
			return <Comment author={comment.author} text={comment.text} key={index} />;
		});
		return (
			<div>
				<h2>Comments</h2>
				{commentNodes}
			</div>
		);
	}
});