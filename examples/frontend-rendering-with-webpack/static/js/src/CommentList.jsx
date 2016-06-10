import React from 'react';
import Comment from './Comment.jsx';

class CommentList extends React.Component {
    clearAll() {
        $.ajax({
            url: '/clear/',
            type: 'GET',
            success: ((response) => {
                renderApp(response);
            })
        })
    }
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
                <button className="btn btn-danger" onClick={this.clearAll}>Clear All</button>
				{commentNodes}
			</div>
		);
	}
}

module.exports = CommentList;
