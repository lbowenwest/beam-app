import React, { Component } from 'react'
import { Link } from 'react-router'


class Home extends Component {
    render() {
        return <div className="jumbotron">
              <h1>Beam App</h1>
              <p className="lead">It's pretty damn awesome</p>
              <p><Link className="btn btn-lg btn-success" to="/app">Check it out</Link></p>
        </div>
    }
}

export default Home