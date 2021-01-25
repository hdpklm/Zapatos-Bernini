import React, { Component } from 'react';
import { Link } from "react-router-dom";

class Cesta extends Component {
	state = {
		productos: []
	}

	componentDidMount() {
		let hand = this.props.handlers;
		hand.ajax("/api/cesta/")
			.done = result => {
				if (result instanceof Array) {
					this.setState({ productos: result })
					hand.cesta_count(result.length)
				}
			}

	}

	handleBorrar = (id) => {
		let hand = this.props.handlers;
		hand.ajax("/api/cesta/" + id, 'delete', { "id": 2 })
			.done = () => this.componentDidMount()
	}

	handleCantidad = (id, count) => {
		let hand = this.props.handlers;
		hand.ajax("/api/cesta/" + id, 'PATCH', { cantidad: count })
			.done = () => this.componentDidMount()
	}

	handleComprar = () => {
		let hand = this.props.handlers;
		hand.ajax("/api/pedido/", 'post')
			.done = () => this.componentDidMount()
	}

	render() {
		let count = this.state.productos.length;
		let content1 = (
			<div>
				<h2>Cesta</h2>
				<p className="article-content">No tienes producton en la cesta!</p>
			</div>
		)
		let content2 = (
			<div>
				<div className="flex">
					<h2>Cesta</h2>
					<div className="button-holder mb-3">
						<p className="article-content">Total: {this.state.productos.map(p => p.total).reduce((a, b) => a + b, 0)}</p>
						<button className="btn btn-warning" onClick={this.handleComprar}>Comprar</button>
					</div>
				</div>
				<div className="content-grid">
					{
						this.state.productos.map(producto =>
							<article key={producto.id} className="media content-section">
								<img className="rounded-circle article-img" width="150" src={producto.imagen} alt="product" />
								<div className="ml-2 media-body">
									<h2><Link className="article-title" to={'producto/' + producto.producto_id}>{producto.nombre}</Link></h2>
									<p className="article-content">Tamaño: {producto.tamanio}</p>
									<p className="article-content">Cantidad: <input type="numver" min="1" max="99" value={producto.cantidad} size="1" onChange={(event) => this.handleCantidad(producto.id, event.target.value)} /></p>
									<p className="article-content">Precio: {producto.precio} Euros</p>
									<p className="article-content">Total: {producto.total} Euros</p>
									<div className="button-holder">
										<button className="btn btn-info" onClick={() => this.handleBorrar(producto.id)}>Borrar</button>
									</div>
								</div>
							</article>
						)
					}
				</div>
			</div>
		);
		let content = (count === 0) ? content1 : content2;
		return (
			<div className="content">
				{content}
			</div>
		);
	}
}

export default Cesta;