import React from 'react';
import logo from './logo.svg';
import amazon_logo from './images/Amazon Logo.png'
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={amazon_logo} className="Amazon-logo" alt="amazon_logo"/>
        <p>
          Welcome to CS 316 Mini Amazon!
        </p>
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>

        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
