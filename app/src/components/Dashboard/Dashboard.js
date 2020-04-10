import React, { Component } from 'react';
import { Button, Container, InputGroup, FormControl } from 'react-bootstrap';
import Select from 'react-select';
import Profile from '../Profile';
import { queryOptions } from '../../constants/options'
import {Column, Table} from 'react-virtualized';
const axios = require('axios');

export default class Dashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            user: null,
            mode: 0,
            uid: null,
        }
    }

    handleOperationSelect = (option) => {
        this.setState({mode: option.value});
    }

    onClick = event => {
        event.preventDefault();
        if (this.state.uid) {
            if (this.state.mode === 0) {
                axios.get('/api/user/' + this.state.uid)
                    .then(response => {
                        this.setState({user: response.data})
                    })
                    .catch(error => {
                        console.log(error);
                    });
            } else if (this.state.mode === 1) {

            } else if (this.state.mode === 2) {

            }
        }
    }

    onChange = event => {
        this.setState({uid: event.target.value});
    }

    render() {
        return (
            <Container style={{textAlign: 'left', marginTop: '20px'}}>
                <InputGroup >
                    <div style={{width: '15%'}}>
                        <Select
                            className="basic-single"
                            classNamePrefix="select"
                            options={queryOptions}
                            defaultValue={queryOptions[0]}
                            onChange={this.handleOperationSelect}
                        />
                    </div>
                    <FormControl type='number' value={this.state.uid || ''} onChange={this.onChange}/>
                    <InputGroup.Append>
                        <Button onClick={this.onClick} variant="outline-secondary" style={{margin: '0px'}}>Submit</Button>
                    </InputGroup.Append>
                </InputGroup>
                <Profile user={this.state.user}/>
            </Container>
        );
    }
}