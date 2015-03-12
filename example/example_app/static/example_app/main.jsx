import React from 'react';
import CommentBox from './components/CommentBox.jsx';

export default (props) => {
	React.render(
		<CommentBox comments={props.comments} url={props.url} pollInterval={props.pollInterval} />,
		document.getElementById('content')
	);
};