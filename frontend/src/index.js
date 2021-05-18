import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter,Switch,Route} from 'react-router-dom';
import {createBrowserHistory} from 'history';

import './index.css';
import App from './components/App';
import Blockchain from './components/Blockchain';
import ConductTransaction from './components/ConductTransaction';

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter history = {createBrowserHistory()}>
      <Switch>
        <Route path="/" exact component={App}/>
        <Route path="/blockchain" component={Blockchain}/>
        <Route path="/transfer" component={ConductTransaction}/>
      </Switch>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);
