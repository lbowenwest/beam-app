import React, { Component } from 'react'
import { Link } from 'react-router'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './App.scss'

class App extends Component {
    render() {
        return (
            <div className="jumbotron">
                <h1>React Router Tutorial</h1>
                <ul role="nav">
                    <li><Link to="/about">About</Link></li>
                    <li><Link to="/repos">Repos</Link></li>
                </ul>
            </div>
        )
    }
}

export default withStyles(App, s)