import React, { Component } from 'react'
import { Link } from 'react-router'

let template = (
    <nav className="navbar navbar-inverse navbar-fixed-top">
        <div className="container">
            <div className="navbar-header">
                <Link className="navbar-brand" to="/">Beam Apps</Link>
            </div>

            <div className="collapse navbar-collapse">
                <ul className="nav navbar-nav">
                    <li><Link to="/" activeClassName="active">Home</Link></li>
                    <li className="dropdown">
                        <a className="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Apps <span className="caret" /></a>
                        <ul className="dropdown-menu">
                            <li><Link to="/app">Beam Calculator</Link></li>
                        </ul>
                    </li>
                </ul>


            </div>
        </div>
    </nav>
)


export default class NavBar extends Component {
    render() {
        return template
    }
}
