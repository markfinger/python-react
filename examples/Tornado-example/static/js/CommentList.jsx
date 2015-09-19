import React from 'react';
import Comment from './Comment.jsx';

class CommentList extends React.Component {
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
}

export default CommentList;
