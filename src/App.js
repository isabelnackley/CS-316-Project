import React from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

// Importing Pages
import './App.css';
import Homepage from "./Homepage"

// Importing Images

import amazon_logo from './images/Amazon Logo.png'

function App() {
  return (
      <Router>
        <div className="app">
            <header className={"App Header"}>
                 <img src={amazon_logo} className="Amazon-logo" alt="amazon_logo"/>}
            </header>
          <Switch>
            <Route path="/">
              <Homepage/>
            </Route>
          </Switch>
        </div>
      </Router>
  );
}

export default App;
