import React from 'react';

class CommentForm extends React.Component {
    submitComment(e) {
        e.preventDefault();
        $.ajax({
            url: '/comment/',
            type: 'POST',
            data: {
                'author': $('#author').val(),
                'text': $('#comment').val()   
            },
            success:((response) => {
                // Re-rendering the app with new props
                renderApp(response);
            }) 
        });
    }
	render() {
		return (
            <form>
                <h2>Submit a comment</h2>
                <div className="form-group">
                    <label>
                        Your name
                        <input id="author" name="author" type="text" className="form-control" placeholder="..." />
                    </label>
                </div>
                <div className="form-group">
                    <label>
                        Say something...
                        <textarea id="comment" name="text" className="form-control" placeholder="..." />
                    </label>
                </div>
                <div className="text-right">
                    <button className="btn btn-primary" onClick={this.submitComment}>Submit</button>
                </div>
            </form>
		);
	}
}

module.exports = CommentForm;
