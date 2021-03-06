import React, { Component } from 'react';
import { Link } from "react-router-dom";

class Login extends Component {
	handleLogin = (event) => {
		event.preventDefault()
		const form = document.getElementById("frmLogin");
		const formData = new FormData(form);
		const hand = this.props.handlers;
		hand.ajax("/api/auth/login/", 'post', formData)
			.done = result => { if (result.token) hand.Login(true, result.token); }

		return false;
	}

	render() {
		return (
			<div className="content">
				<div className="content-section">
					<form id="frmLogin" onSubmit={this.handleLogin}>
						<fieldset className="form-group">
							<legend className="border-bottom mb-4">Iniciar sesión</legend>
							<div className="row">
								<div className="col-md-6 col-md-offset-3">
									<div className="form-group">
										<label htmlFor="username">Nombre de usuario:</label>
										<input name="username" />
									</div>
								</div>
							</div>
							<div className="row">
								<div className="col-md-6 col-md-offset-3">
									<div className="form-group">
										<label htmlFor="password">Contraseña:</label>
										<input name="password" type="password" />
									</div>
								</div>
							</div>
						</fieldset>
						<div className="form-group">
							<button className="btn btn-outline-info" type="submit">Iniciar sesión</button>
						</div>
					</form>
					<div className="border-top pt-3">
						<small className="text-muted">
							<Link className="ml-2" to="/register">Registrate ahora</Link>
						</small>
					</div>
				</div>
			</div>
		);
	}
}

export default Login;