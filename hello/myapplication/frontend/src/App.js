import React, { useEffect } from "react";
import logo from './logo.svg';
import './App.css';

function App() {
  useEffect(() => {
    fetch("http://192.168.1.4:8000")
      .then(res => res.json())
      .then(data => {
        console.log(data);   // backend response
      })
      .catch(err => console.error(err));
  }, []);


  return (
    <div className="App">
      <header className="App-header">
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
