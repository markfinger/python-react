import React from 'react';
import $ from 'jquery';
import CommentList from './CommentList.jsx';
import CommentForm from './CommentForm.jsx';

export default React.createClass({
	getInitialState() {
		return {comments: this.props.comments};
	},
	handleCommentSubmit(comment) {
		var comments = this.state.comments;
		comments.push(comment);
		this.setState({comments: comments}, () => {
			this.postComment(comment);
		});
	},
	postComment(comment) {
		$.ajax({
			url: this.props.url,
			type: 'POST',
			dataType: 'json',
			data: comment,
			success: (data) => {
				this.setState({comments: data.comments});
			},
			error: (xhr, status, err) => {
				console.error(this.props.url, status, err.toString());
			}
		});
	},
	getComments() {
		$.ajax({
			url: this.props.url,
			dataType: 'json',
			success: (data) => {
				this.setState({comments: data.comments});
			},
			error: (xhr, status, err) => {
				console.error(this.props.url, status, err.toString());
			},
			complete: this.pollForNewComments
		});
	},
	pollForNewComments() {
		setTimeout(this.getComments, this.props.pollInterval);
	},
	componentDidMount() {
		this.pollForNewComments();
	},
	render() {
		return (
			<div>
				<CommentList comments={this.state.comments} />
				<CommentForm url={this.props.url} onCommentSubmit={this.handleCommentSubmit} />
			</div>
		);
	}
});