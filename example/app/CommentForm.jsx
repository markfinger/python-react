import React from 'react';

class CommentForm extends React.Component {
	render() {
		return (
			<form method="post" action={this.props.url}>
				<h2>Submit a comment</h2>
				<div className="form-group">
					<label>
						Your name
						<input name="author" type="text" className="form-control" placeholder="..." />
					</label>
				</div>
				<div className="form-group">
					<label>
						Say something...
						<textarea name="text" className="form-control" placeholder="..." />
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