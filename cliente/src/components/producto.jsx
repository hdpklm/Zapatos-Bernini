import React, { Component } from 'react';
// import { useParams } from "react-router-dom";

class Producto extends Component {

	state = {
		producto: {}
	}

	componentDidMount() {
		let hand = this.props.handlers
		hand.ajax("/api/producto/" + this.props.pp.match.params.id)
			.done = result => {
				this.setState({ producto: result });
				// todo // hand.cesta_count(result.cesta_count)
			}
	}

	handleAniadir = (id) => {
		let hand = this.props.handlers
		hand.ajax("/api/cesta/", 'post', { producto: id })
			.done = result => 0 // todo // hand.cesta_count(result.count)
	}

	render() {
		const producto = this.state.producto;

		return (
			<div className="content">
				<div className="content">
					<h2>Producto: {producto.nombre}</h2>
					<div className="content mt-4">
						<article className="media content">
							<img className="rounded-circle article-img" width="200" src={producto.imagen} alt="product" />
							<div className="ml-2 media-body">
								<p className="article-content">Tamaño: {producto.tamanio}</p>
								<p className="article-content">Precio: {producto.precio} Euros</p>
								<button className="btn btn-info" onClick={() => this.handleAniadir(producto.id)}>Añadir a la cesta</button>
								<p className="article-content">
									Descripcion:
									<div className="description">
										{producto.desc}
									</div>
								</p>
							</div>
						</article>
					</div>
				</div>
			</div>
		);
	}
}

export default Producto;