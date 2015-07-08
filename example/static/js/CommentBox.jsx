import React from 'react';
import CommentList from './CommentList.jsx';
import CommentForm from './CommentForm.jsx';

class CommentBox extends React.Component {
	render() {
		return (
			<div>
				<CommentList comments={this.props.comments} />
				<CommentForm url={this.props.url} />
			</div>
		);
	}
}

export default CommentBox;