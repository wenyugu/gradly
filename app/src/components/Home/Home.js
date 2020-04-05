import React, { Component } from 'react';
import { Container, Row, Col, Jumbotron} from 'react-bootstrap';
import DataEntry from '../DataEntry';
  
export default class Home extends Component {

    render() {
        return (
            <Container>
                <Row>
                    <Col>
                    <Jumbotron>
                        <h4>Get started by entering your previous work and education experience.</h4>
                    </Jumbotron>
                    <DataEntry/>
                    </Col>
                    <Col>
                    
                    </Col>
                </Row>
            </Container>
      );
    }
}