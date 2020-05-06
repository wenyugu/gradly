import React, { Component } from 'react';
import { Button, Container, InputGroup, FormControl, Jumbotron, Form, Col, Row, Table, Alert } from 'react-bootstrap';
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
            industry: '',
            title: '',
            edittable: false,
            error: 0,
            success: false,
            checkNum: -1,
            courseRec: {},
            jobRec: []
        }
    }

    handleOperationSelect = (option) => {
        this.setState({mode: option.value, edittable: false, success: false});
    }

    getUser = () => {
        axios.get('/api/user/' + this.state.uid)
            .then(response => {
                this.setState({ user: response.data, edittable: true, error: 0 });
            })
            .catch(error => {
                console.log(error);
                this.setState({ user: null, edittable: false, error: 1 });
            });
    }

    updateUser = user => {
        axios.post('/api/user/' + this.state.uid, user)
            .then(response => {
                console.log(response.data);
                this.setState({ error: 0, success: true });
            })
            .catch(error => {
                console.log(error);
                this.setState({ error: 1 });
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
                        this.setState({ error: 0, success: true });
                    })
                    .catch(error => {
                        console.log(error);
                        this.setState({ error: 1 });
                    });
            } else if (this.state.mode === 3) {
                if (this.state.checkNum === 0) {
                    const params = { userID: this.state.uid };
                    axios.get('/api/query/careers', { params: params })
                        .then(response =>{
                            this.setState({ jobRec: response.data.results, error: 0 });
                        })
                        .catch(error => {
                            console.log(error);
                            this.setState({ error: 1, jobRec: [] });
                        })
                }
            }
        }
        if (this.state.mode === 3 && this.state.checkNum === 1) {
            var params;
            if (this.state.title) {
                params = { industry: this.state.industry, title: this.state.title };
            } else {
                params = { industry: this.state.industry };
            }
            axios.get('/api/query/courses', { params: params })
                .then(response => {
                    console.log(response.data)
                    this.setState({ courseRec: response.data, error: 0 });
                })
                .catch(error => {
                    console.log(error);
                    this.setState({ error: 2, courseRec: {} });
                })
        }
    }

    handleChange = event => {
        this.setState({[event.target.name]: event.target.value});
    }

    render() {
        return (
            <Container style={{textAlign: 'left', marginTop: '20px'}}>
                {this.state.mode === 3 ? (
                    <Jumbotron fluid>
                    <Container>
                      <h1>Supported Queries</h1>
                      <p>
                        1. Enter your UserID to find out job recommendations based on your provided background.
                      </p>
                      <p>
                        2. Enter a target industry and job title (optional) to find out course recommendations.
                      </p>
                    </Container>
                  </Jumbotron>
                ) : null }
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
                    <FormControl type='number' name='uid' value={this.state.uid || ''} placeholder='userID' onChange={this.handleChange}/>
                    {
                        this.state.mode === 3 ? (
                            <>
                                <FormControl type='text' name='industry' value={this.state.industry} placeholder='Desired industry: Ex. Internet' onChange={this.handleChange} />
                                <FormControl type='text' name='title' value={this.state.title} placeholder='Desired position: Ex. Engineer' onChange={this.handleChange} />
                            </>

                        ) : null
                    }
                    <InputGroup.Append>
                        <Button onClick={this.onClick} variant="outline-secondary" style={{margin: '0px'}}>{this.state.mode === 1 ? 'Edit' : 'Submit'}</Button>
                    </InputGroup.Append>
                </InputGroup>
                {
                    this.state.mode === 3 ? (
                        <Form>
                            <fieldset>
                                <Form.Group as={Row}>
                                    <Col sm={10}>
                                        <Form.Check
                                            type="radio"
                                            label="Jobs"
                                            name="checkNum"
                                            id="option1"
                                            value={0}
                                            onChange={this.handleChange}
                                        />
                                        <Form.Check
                                            type="radio"
                                            label="Courses"
                                            name="checkNum"
                                            id="option2"
                                            value={1}
                                            onChange={this.handleChange}
                                        />
                                    </Col>
                                    </Form.Group>
                            </fieldset>
                        </Form>
                    ) : null
                }
                { this.state.error === 1 ? (<Alert variant="danger">UserID not found.</Alert>) : null }
                { this.state.error === 2 ? (<Alert variant="danger">Something went wrong.</Alert>) : null }
                { this.state.mode === 1 && this.state.success ? (<Alert variant="success">Successfully updated user.</Alert>) : null }
                { this.state.mode === 2 && this.state.success ? (<Alert variant="success">Successfully deleted user.</Alert>) : null }
                { this.state.mode === 0 && this.state.user && <Profile user={this.state.user} /> }
                { this.state.edittable && this.state.mode === 1 && this.state.user && <DataEntry user={this.state.user} update={this.updateUser}/> }
                { this.state.mode === 3 && this.state.checkNum === 0 && this.state.jobRec &&
                <Table>
                    <tbody>
                        { this.state.jobRec.map((el, idx) => (
                            <tr key={`${el}~${idx}`}>
                                <td>{el.role}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table> }
                { this.state.mode === 3 && this.state.checkNum === 1 && this.state.courseRec &&
                <Table>
                        { Object.keys(this.state.courseRec).map((el, idx) => (
                            <>
                            <thead key={`${el}~${idx}`}>
                                <tr>
                                    <th>{el}</th>
                                </tr>
                            </thead>
                            <tbody>
                                {this.state.courseRec[el].map((item, i) => (
                                    <tr key={`${item}~${i}`}>
                                        <td>{item}</td>
                                    </tr>
                                ))}
                            </tbody>
                            </>
                        ))
                        }
                </Table> }
            </Container>
        );
    }
}
