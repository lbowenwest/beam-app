import React, { Component } from 'react'
import {render} from 'react-dom'
import {IndexRoute, Route, Router, browserHistory, Link} from 'react-router'

import App from './components/App'
import Home from './components/Home'

import Beam from './apps/Beam'

render((
  <Router history={browserHistory}>
    <Route path="/" component={App}>
      <IndexRoute component={Home}/>
      <Route path="app" component={Beam} />
    </Route>
  </Router>
), document.getElementById('app'))