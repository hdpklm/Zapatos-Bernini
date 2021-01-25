import React from 'react';
import { Link } from "react-router-dom";

const NavBar = (props) => {
	let user_profile = "";
	if (props.data.isLogin === "true") {
		user_profile = (
			<div className="navbar-nav">
				<Link className="nav-item nav-link" to="/cesta">
					Cesta
					<span className="badge badge-pill badge-danger">{props.data.cesta_count}</span>
				</Link>
				<Link className="nav-item nav-link" to="/pedidos">Pedidos</Link>
				<Link className="nav-item nav-link" to="/logout">Logout</Link>
			</div>
		)
	} else {
		user_profile = (
			<div className="navbar-nav">
				<Link className="nav-item nav-link" to="/login">Login</Link>
				<Link className="nav-item nav-link" to="/register">Register</Link>
			</div>
		)
	}

	return (
		<div className="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
			<div className="container">
				<Link className="navbar-brand mr-4" to="/">Zapatos Bernini</Link>
				<button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
					<span className="navbar-toggler-icon"></span>
				</button>
				<div className="collapse navbar-collapse" id="navbarToggle">
					<div className="navbar-nav mr-auto">
						<Link className="nav-item nav-link" to="/">Home</Link>
					</div>

					<div className="navbar-nav">
						{user_profile}
					</div>
				</div>
			</div>
		</div>
	);

}

export default NavBar;