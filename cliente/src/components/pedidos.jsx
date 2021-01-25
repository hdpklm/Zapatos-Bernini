import React, { Component } from 'react';
import { Link } from "react-router-dom";

class Pedidos extends Component {
	state = {
		pedidos: []
	}

	componentDidMount() {
		let hand = this.props.handlers;
		hand.ajax("/api/pedidos/")
			.done = result => {
				if (result instanceof Array) {
					this.setState({ pedidos: result })
				}
			}
	}

	render() {
		return (
			<div className="content">
				<h2>Tus pedidos</h2>
				<div className="content-flex"> {
					this.state.pedidos.map(pedido =>
						<article key={pedido.id} className="content-section">
							<h2>Pedido numero #{pedido.id}</h2>
							<p className="article-content">Precio Total: {
								pedido.productos.map(p => p.total)
									.reduce((a, b) => a + b, 0)
							} Euros</p>
							<p className="article-content">Fetcha: {pedido.date.toString("F d, Y")}</p>
							<div className="producto-holder">
								<div className="producto">
									<span>Producto</span>
									<span>Cantidad</span>
									<span>Precio</span>
									<span>Total</span>
								</div> {
									pedido.productos.map(producto =>
										<Link key={producto.id} className="article-title" to={'producto/' + producto.producto_id}>
											<div className="producto">
												<span>{producto.nombre}</span>
												<span>{producto.cantidad}</span>
												<span>{producto.precio}</span>
												<span>{producto.total}</span>
											</div>
										</Link>
									)
								}
							</div>
						</article>
					)
				}
				</div>
			</div>
		);
	}
}

export default Pedidos;