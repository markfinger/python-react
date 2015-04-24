import React from 'react';

export default React.createClass({
	handleSubmit(e) {
		e.preventDefault();
		var author = this.refs.author.getDOMNode().value.trim();
		var text = this.refs.text.getDOMNode().value.trim();
		if (!text || !author) {
			return;
		}
		this.props.onCommentSubmit({author: author, text: text});
		this.refs.author.getDOMNode().value = '';
		this.refs.text.getDOMNode().value = '';
	},
	render() {
		return (
			<form method="POST" action={this.props.url} onSubmit={this.handleSubmit}>
				<h2>Submit a comment</h2>
				<div className="form-group">
					<label>
						Your name
						<input type="text" className="form-control" name="author" ref="author" />
					</label>
				</div>
				<div className="form-group">
					<label>
						Say something...
						<textarea className="form-control" name="text" ref="text" />
					</label>
				</div>
				<div className="text-right">
					<button type="reset" className="btn btn-default">Reset</button>
					<button type="submit" className="btn btn-primary">Submit</button>
				</div>
			</form>
		);
	}
});