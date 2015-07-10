import React from 'react';
import Comment from './Comment.jsx';

class CommentList extends React.Component {
	render() {
		if (!this.props.comments.length) {
			return null;
		}
		return (
			<div>
				<h2>Comments</h2>
				{this.props.comments.map((comment, index) => {
					return <Comment name={comment.name} text={comment.text} key={index} />;
				})}
			</div>
		);
	}
}

export default CommentList;