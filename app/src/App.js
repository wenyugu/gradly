import React, { Component } from 'react';
import { Nav, Navbar } from 'react-bootstrap';
import './App.css';
import {
    Switch,
    Route,
    Link
} from "react-router-dom";
import Home from './components/Home';
import Dashboard from './components/Dashboard';

class App extends Component {

  render() {
      return (
          <div className="App">
              <Navbar bg="light" expand="lg">
                  <Navbar.Brand as={Link} to="/">Gradly</Navbar.Brand>
                  <Navbar.Toggle aria-controls="basic-navbar-nav" />
                  <Navbar.Collapse id="basic-navbar-nav">
                      <Nav className="mr-auto">
                          <Nav.Link as={Link} to="/dashboard">Dashboard</Nav.Link>
                      </Nav>
                  </Navbar.Collapse>
              </Navbar>
              <Switch>
                  <Route exact path="/dashboard">
                      <Dashboard />
                  </Route>
                  <Route exact path="/">
                      <Home />
                  </Route>
              </Switch>
          </div>
      );
  }
}

export default App;
