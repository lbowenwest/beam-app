import React, { Component } from 'react';
import { render } from 'react-dom';
import { Router, Route, hashHistory } from 'react-router';

import App from './components/App';
import Repos from './components/Repos';
import About from './components/About';

render((
    <Router history={hashHistory}>
        <Route path="/" component={App} />
        <Route path="/repos" component={Repos} />
        <Route path="/about" component={About} />
    </Router>
), document.getElementById('beam-app'));
