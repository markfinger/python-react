// CSS dependencies
import 'bootstrap/dist/css/bootstrap.css';
import './CommentBox.css';

import React from 'react';
import CommentList from './CommentList.jsx';
import CommentForm from './CommentForm.jsx';
import $ from 'jquery';

class CommentBox extends React.Component {
	constructor(props) {
		super(props);

		this.state = {comments: props.comments};
	}
	submitComment(name, text) {
		$.ajax({
			url: this.props.url,
			method: 'post',
			data: {
				name,
				text
			},
			success: (obj) => {
				this.setState({
					comments: obj.comments
				});
			},
			error: (err) => {
				console.error(err);
			}
		});
	}
	render() {
		return (
			<div>
				<CommentList comments={this.state.comments} />
				<CommentForm submitComment={this.submitComment.bind(this)} />
			</div>
		);
	}
}

export default CommentBox;