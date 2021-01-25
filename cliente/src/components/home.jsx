import React, { Component } from 'react';
import { Link } from "react-router-dom";

class Home extends Component {
	state = {
		productos: []
	}

	componentDidMount() {
		let hand = this.props.handlers
		hand.ajax("/api/productos/")
			.done = result => {
				this.setState({ productos: result });
				// todo // hand.cesta_count(result.cesta_count)
			}
	}

	handleAniadir = (id) => {
		let hand = this.props.handlers
		hand.ajax("/api/cesta/", 'post', { producto: id })
			.done = result => 0 // todo // hand.cesta_count(result.count)
	}

	render() {
		return (
			<div className="content">
				<div className="content-grid">
					{
						this.state.productos.map(producto =>
							<article key={producto.id} className="media content-section">
								<img className="rounded-circle article-img" width="150" src={producto.imagen} alt="product" />
								<div className="ml-2 media-body">
									<h2><Link className="article-title" to={"producto/" + producto.id}>{producto.nombre}</Link></h2>
									<p className="article-content">Tamaño: {producto.tamanio}</p>
									<p className="article-content">Precio: {producto.precio} Euros</p>
									<button className="btn btn-info" onClick={() => this.handleAniadir(producto.id)}>Añadir a la Cesta</button>
								</div>
							</article>
						)
					}
				</div>
			</div>
		);
	}
}

export default Home;