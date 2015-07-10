import React from 'react';

class CommentForm extends React.Component {
	handleSubmit(event) {
		event.preventDefault();

		var name = this.refs.name.getDOMNode().value.trim();
		var text = this.refs.text.getDOMNode().value.trim();

		this.props.submitComment(name, text);
	}
	render() {
		return (
			<form onSubmit={this.handleSubmit.bind(this)}>
				<h2>Submit a comment</h2>
				<div className="form-group">
					<label>
						Your name
						<input ref="name" type="text" className="form-control" placeholder="..." />
					</label>
				</div>
				<div className="form-group">
					<label>
						Say something...
						<textarea ref="text" className="form-control" placeholder="..." />
					</label>
				</div>
				<div className="text-right">
					<button type="reset" className="btn btn-default">Reset</button>
					<button type="submit" className="btn btn-primary">Submit</button>
				</div>
			</form>
		);
	}
}

export default CommentForm;