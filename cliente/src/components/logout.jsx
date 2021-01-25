import React, { Component } from 'react';
import { Link } from "react-router-dom";

class Logout extends Component {
	componentDidMount() {
		let hand = this.props.handlers;
		if (this.props.data.isLogin) {
			let ajax = hand.ajax("/api/auth/logout/", "post")
			ajax.done = (r) => {
				hand.Login(false);
			}
		}
	}

	render() {
		return (
			<div className="content">
				<div className="content-section">
					<h2>Has cerrado la sesión</h2>
					<div className="border-top pt-3">
						<small className="text-muted">
							<Link to="/login">Iniciar sesión</Link>
						</small>
					</div>
				</div>
			</div>
		);
	}
}

export default Logout;