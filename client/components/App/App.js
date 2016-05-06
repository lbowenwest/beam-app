import React, { Component } from 'react'

import s from './App.scss'
import NavBar from '../NavBar'

class App extends Component {
    render() {
        return <div className="container">
            <NavBar />
            <div className="container" id="content">
                {this.props.children}
            </div>
        </div>
    }
}

// export default withStyles(App, s)
export default App