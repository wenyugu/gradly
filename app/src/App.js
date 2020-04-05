import React, { Component } from 'react';
import { Nav, Navbar } from 'react-bootstrap';
import './App.css';
import Home from './components/Home';

class App extends Component {

  render() {
      return (
          <div className="App">
              <Navbar bg="light" expand="lg">
                  <Navbar.Brand href="/">Gradly</Navbar.Brand>
                  <Navbar.Toggle aria-controls="basic-navbar-nav" />
                  <Navbar.Collapse id="basic-navbar-nav">
                      <Nav className="mr-auto">
                          <Nav.Link href="/data">Data</Nav.Link>
                      </Nav>
                  </Navbar.Collapse>
              </Navbar>
              <Home/>
          </div>
      );
  }
}

export default App;
