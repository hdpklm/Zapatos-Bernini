import React, { Component } from 'react';
import Home from "./components/home"
import Cesta from "./components/cesta"
import Producto from "./components/producto"
import Pedidos from "./components/pedidos"
// import PedidoDetalle from "./components/pedido_detalle"
import Login from "./components/login"
import Logout from "./components/logout"
import Register from "./components/register"
import NavBar from './components/navbar';
import Messages from './components/messages';
import {
  Route,
  Switch,
  BrowserRouter
} from "react-router-dom";

class App extends Component {
  server_link = "http://127.0.0.1:8000"

  state = {
    token: localStorage.token,
    isLogin: localStorage.isLogin,
    messages: [],
    cesta_count: 0,
  }

  constructor(props) {
    super(props);
    this.handle.ajax = this.handle.ajax.bind(this);
    this.handle.Login = this.handle.Login.bind(this);
    this.handle.notify = this.handle.notify.bind(this);
    this.handle.removeAlert = this.handle.removeAlert.bind(this);
    this.handle.deleteAlert = this.handle.deleteAlert.bind(this);
    this.handle.cesta_count = this.handle.cesta_count.bind(this);
  }

  componentDidMount() {
    if (this.state.isLogin !== "true") return

    let hand = this.handle
    hand.ajax("/api/cesta/")
      .done = result => {
        hand.cesta_count(result.length)
      }
  }

  handle = {
    Login(isLogin, token = null) {
      if (isLogin) {
        localStorage.token = token;
        localStorage.isLogin = isLogin;
        window.location = "/";
      } else {
        localStorage.removeItem("token");
        localStorage.isLogin = false;
      }
      const data = Object.assign({}, this.state);
      data.token = token;
      data.isLogin = isLogin;
      this.setState(data)
    },

    cesta_count(count) {
      const state = Object.assign({}, this.state);
      state.cesta_count = count;
      this.setState(state)
    },

    notify(type, message) {
      let nthis = this;
      let msg = { type, message };
      let state = Object.assign({}, this.state);
      state.messages.push(msg);
      this.setState(state);

      setTimeout(() => {
        let index = nthis.state.messages.indexOf(msg);
        nthis.handle.removeAlert(index);
      }, 15000);
    },

    removeAlert(index) {
      if (!this.state.messages[index]) return

      let nthis = this;
      let state = Object.assign({}, this.state);
      state.messages[index].remove = true;
      this.setState(state);
      setTimeout(() => {
        nthis.handle.deleteAlert(index);
      }, 200);
    },

    deleteAlert(index) {
      if (!this.state.messages[index]) return

      let state = Object.assign({}, this.state);
      delete state.messages[index];
      this.setState(state);
    },

    ajax(url, method = "get", body = null, done = null) {
      const headers = {}
      if (this.state.token) {
        headers["Authorization"] = "token " + this.state.token
      }

      if (body instanceof FormData) {
        // do nothing
      } else if (typeof body === "string") {
        headers["Content-Type"] = "application/json"
      } else if (typeof body === "object" && body != null) {
        headers["Content-Type"] = "application/json"
        body = JSON.stringify(body)
      }

      let ajax = { done }

      fetch(url, { method, body, headers })
        .then(res => res.json())
        .then(
          (result) => {
            if (result.info) this.handle.notify("info", result.info)
            if (result.detail) this.handle.notify("danger", result.detail)
            if (result.success) this.handle.notify("success", result.success)
            if (result.warning) this.handle.notify("warning", result.warning)
            if (result.cesta_count) this.handle.cesta_count(result.cesta_count)
            if (result.non_field_errors) this.handle.notify("danger", result.non_field_errors)
            if (result.error) {
              if (result.error instanceof Array) {
                for (let error of result.error)
                  this.handle.notify("danger", error)
              } else {
                this.handle.notify("danger", result.error)
              }
            }

            if (typeof ajax.done === "function") {
              ajax.done(result);
            }
          },
          (error) => {
            this.handle.notify("danger", error.message)
          }
        )

      return ajax;
    }
  }

  render() {
    const data = this.state;
    return (
      <BrowserRouter>
        <NavBar data={data} />
        <Messages data={data} handlers={this.handle} />
        <Switch>
          <Route path="/cesta">
            <Cesta data={data} handlers={this.handle} />
          </Route>

          <Route path="/pedidos">
            <Pedidos data={data} handlers={this.handle} />
          </Route>

          <Route path="/producto/:id" render={props => <Producto data={data} pp={props} handlers={this.handle} />} />

          <Route path="/login">
            <Login data={data} handlers={this.handle} />
          </Route>

          <Route path="/logout">
            <Logout data={data} handlers={this.handle} />
          </Route>

          <Route path="/register">
            <Register data={data} handlers={this.handle} />
          </Route>

          <Route path="/">
            <Home data={data} handlers={this.handle} />
          </Route>

        </Switch>
      </BrowserRouter >
    );
  }
}

export default App;
