import React, { Component } from 'react';
import { Container, Jumbotron} from 'react-bootstrap';
import DataEntry from '../DataEntry';
  
export default class Home extends Component {

    render() {
        return (
            <Container style={{maxWidth: '50%'}}>
                <Jumbotron>
                    <h4>Get started by entering your previous work and education experience.</h4>
                </Jumbotron>
                <DataEntry />
            </Container>
      );
    }
}