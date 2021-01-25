const Message = props => {
	let hand = props.handlers;
	let msgs = props.data.messages;
	if (msgs.length > 0) {
		return (
			<div className="message-holder">
				{msgs.map((message, i) => (
					<div key={i} className={`alert alert-dismissible alert-${message.type} ${message.remove ? "removing" : ""}`}>
						<div className="close" onClick={() => hand.removeAlert(i)}>x</div>
						{message.message}
					</div>
				))}
			</div>
		);
	}

	return null;
}

export default Message;