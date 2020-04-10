import React, { Component } from 'react';
import { Button, Container, InputGroup, FormControl } from 'react-bootstrap';
import Select from 'react-select';
import Profile from '../Profile';
import DataEntry from '../DataEntry';
import { queryOptions } from '../../constants/options'
const axios = require('axios');

export default class Dashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            user: null,
            mode: 0,
            uid: null,
            edittable: false,
        }
    }

    handleOperationSelect = (option) => {
        this.setState({mode: option.value, edittable: false});
    }

    getUser = () => {
        axios.get('/api/user/' + this.state.uid)
            .then(response => {
                this.setState({ user: response.data, edittable: true })
            })
            .catch(error => {
                console.log(error);
            });
    }

    updateUser = user => {
        axios.post('/api/user/' + this.state.uid, user)
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    onClick = event => {
        event.preventDefault();
        if (this.state.uid) {
            if (this.state.mode === 0) {
                this.getUser();
            } else if (this.state.mode === 1) {
                this.getUser();
                
            } else if (this.state.mode === 2) {
                axios.delete('/api/user/' + this.state.uid)
                    .then(response => {
                        console.log(response.data);
                    })
                    .catch(error => {
                        console.log(error);
                    });
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
                        <Button onClick={this.onClick} variant="outline-secondary" style={{margin: '0px'}}>{this.state.mode === 1 ? 'Edit' : 'Submit'}</Button>
                    </InputGroup.Append>
                </InputGroup>
                {
                    this.state.edittable && this.state.mode === 1? (
                        <DataEntry user={this.state.user} update={this.updateUser}/>
                    ) : (
                        <Profile user={this.state.user}/>
                    )
                }
            </Container>
        );
    }
}