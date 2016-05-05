import React, { Component } from 'react';
import { render } from 'react-dom';
import { Router, Route, browserHistory } from 'react-router';

import App from './components/App';
import Repos from './components/Repos';
import About from './components/About';

alert('Hello you')

render((
    <Router history={browserHistory}>
        <Route path="/" component={App} />
        <Route path="/repos" component={Repos} />
        <Route path="/about" component={About} />
    </Router>
), document.getElementById('beam-app'));
