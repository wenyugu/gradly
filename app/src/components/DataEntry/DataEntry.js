import React, { Component, Fragment } from 'react';
import { Accordion, Button, Card, Form, Row, Col } from 'react-bootstrap';
import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';
import './DataEntry.css';
import { empOptions, degreeOptions, industryOptions, institutionOptions, skillsOptions, salaryOptions } from '../../constants/options';
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import RangeSlider from 'react-bootstrap-range-slider';

const selectStyles = {
    menuPortal: base => ({ ...base, zIndex: 9999 }),
    menu: provided => ({ ...provided, zIndex: "9999 !important" })
};

export default class DataEntry extends Component {
    constructor(props) {
        super(props);
        var year = new Date().getFullYear() + 4;
        this.years = Array.from(new Array(100),(val, index) => year - index);
        this.state = {
            education: [{
                school: '',
                degree: '',
                major: '',
                gpa: 0,
                year: 1900,
                courses: [{num: 0, name: ''}]
            }],
            experience: [{
                order: 0,
                employer: '',
                industry: '',
                title: '',
                salary: 0,
                type: '',
                rating: 0,
            }],
            skills: []
        };
    }

    addEducation = () => {
        const values = [...this.state.education];
        values.push({
            school: '',
            degree: '',
            major: '',
            gpa: 0,
            year: 1900,
            courses: [{ num: 0, name: '' }]
            }
        );
        this.setState({education: values});
    }

    removeEducation = index => {
        const values = [...this.state.education];
        values.splice(index, 1);
        this.setState({ education: values });
    };

    addCourse = index => {
        const values = [...this.state.education];
        values[index].courses.push({num: 0, name: ''});
        this.setState({ education: values });
    };

    removeCourse = (num, index) => {
        const values = [...this.state.education];
        values[num].courses.splice(index, 1);
        this.setState({ education: values });
    }

    addExperience = () => {
        const values = [...this.state.experience];
        values.push({
            order: 0,
            employer: '',
            industry: '',
            title: '',
            salary: 0,
            type: '',
            rating: 0,
        }
        );
        this.setState({experience: values});
    }

    removeExperience = index => {
        const values = [...this.state.experience];
        values.splice(index, 1);
        this.setState({ experience: values });
    };

    handleRatingChange = (e, idx) => {
        const values = [...this.state.experience];
        values[idx].rating = e.target.value;
        this.setState({ experience: values });
    }

    render() {
        return (
            <div>

                <Accordion defaultActiveKey="0" style={{'text-align': 'left'}}>
                    <Card>
                        <Accordion.Toggle as={Card.Header} variant="link" eventKey="0">
                            Education
                        </Accordion.Toggle>
                        <Accordion.Collapse eventKey="0">
                            <Card.Body>
                                <Form >
                                    {
                                        this.state.education.map((el, idx) => (
                                            <Fragment>
                                                <Button variant="dark" className='float-right' size='sm' onClick={() => this.removeEducation(idx)}>—</Button>
                                                <Form.Group>
                                                    <Form.Label style={{'margin-bottom': '18px'}}>School</Form.Label>
                                                    <CreatableSelect
                                                        menuPortalTarget={document.querySelector('body')}
                                                        styles={selectStyles}
                                                        options={institutionOptions}
                                                    />
                                                </Form.Group>
                                                <Form.Group >
                                                    <Form.Label>Degree</Form.Label>
                                                    <Select
                                                        className="basic-single"
                                                        classNamePrefix="select"
                                                        isClearable
                                                        isSearchable
                                                        menuPortalTarget={document.querySelector('body')}
                                                        styles={selectStyles}
                                                        options={degreeOptions}
                                                    />
                                                </Form.Group>
                                                <Row>
                                                    <Col>
                                                        <Form.Group>
                                                            <Form.Label>Major</Form.Label>
                                                            <Form.Control placeholder="Major" />
                                                        </Form.Group>
                                                    </Col>
                                                    <Col>
                                                        <Form.Group>
                                                            <Form.Label>GPA</Form.Label>
                                                            <Form.Control placeholder="GPA: Optional" />
                                                        </Form.Group>
                                                    </Col>
                                                </Row>
                                                <Form.Group >
                                                    <Form.Label>Graduation Year</Form.Label>
                                                    <Form.Control as="select" value="Choose...">
                                                        {
                                                            this.years.map((year, index) => {
                                                                return <option key={`year${index}`} value={year}>{year}</option>
                                                            })
                                                        }
                                                    </Form.Control>
                                                </Form.Group>
                                                <Form.Label>Courses</Form.Label>
                                                {
                                                    this.state.education[idx].courses.map((elem, index) => (
                                                        <Fragment>
                                                            <Button variant="dark" className='float-right' size='sm' onClick={() => this.removeCourse(idx, index)}>—</Button>
                                                            <Row>
                                                                <Col>
                                                                    <Form.Group>
                                                                        <Form.Label>Course Name</Form.Label>
                                                                        <Form.Control placeholder="Ex. Database Systems" />
                                                                    </Form.Group>
                                                                </Col>
                                                                <Col>
                                                                    <Form.Group>
                                                                        <Form.Label>Course Number</Form.Label>
                                                                        <Form.Control placeholder="Ex. CS411" />
                                                                    </Form.Group>
                                                                </Col>
                                                            </Row>
                                                        </Fragment>
                                                    ))
                                                }
                                                <Button variant="secondary" onClick={() => this.addCourse(idx)}>Add another course</Button>
                                            </Fragment>
                                        ))
                                    }
                                    <div>
                                        <Button variant="primary" onClick={this.addEducation}>Add education</Button>
                                    </div>
                                </Form>
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                    <Card>
                        <Accordion.Toggle as={Card.Header} variant="link" eventKey="2">
                            Experience
                        </Accordion.Toggle>
                        <Accordion.Collapse eventKey="2">
                            <Card.Body>
                                <Form>
                                    {
                                        this.state.experience.map((el, idx) => (
                                            <Fragment>
                                                <Button variant="dark" className='float-right' size='sm' onClick={() => this.removeExperience(idx)}>—</Button>
                                                <Form.Group>
                                                    <Form.Label>Employer</Form.Label>
                                                    <Form.Control placeholder="Ex. Google" />
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Title</Form.Label>
                                                    <Form.Control placeholder="Ex. Software Engineer" />
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Employment Type</Form.Label>
                                                    <Select
                                                        className="basic-single"
                                                        classNamePrefix="select"
                                                        isClearable
                                                        isSearchable
                                                        menuPortalTarget={document.querySelector('body')}
                                                        styles={selectStyles}
                                                        options={empOptions}
                                                    />
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Industry</Form.Label>
                                                    <CreatableSelect
                                                        isMulti
                                                        menuPortalTarget={document.querySelector('body')}
                                                        styles={selectStyles}
                                                        options={industryOptions}
                                                    />
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Salary Range</Form.Label>
                                                    <Select
                                                        className="basic-single"
                                                        classNamePrefix="select"
                                                        isClearable
                                                        menuPortalTarget={document.querySelector('body')}
                                                        styles={selectStyles}
                                                        options={salaryOptions}
                                                    />
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Rating</Form.Label>
                                                    <RangeSlider value={this.state.experience[idx].rating} onChange={e => this.handleRatingChange(e, idx)} max={10} />
                                                </Form.Group>
                                            </Fragment>
                                        ))
                                    }
                                    <div>
                                        <Button variant="primary" onClick={this.addExperience}>Add experience</Button>
                                    </div>
                                </Form>
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                    <Card>
                        <Accordion.Toggle as={Card.Header} variant="link" eventKey="3">
                            Skills
                        </Accordion.Toggle>
                        <Accordion.Collapse eventKey="3">
                            <Card.Body>
                                <Form>
                                    <Form.Group>
                                        <Form.Label>Skills</Form.Label>
                                        <CreatableSelect
                                            isMulti
                                            menuPortalTarget={document.querySelector('body')}
                                            styles={selectStyles}
                                            options={skillsOptions}
                                        />
                                    </Form.Group>
                                </Form>
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                </Accordion>
                <Card>
                    <Button>Submit</Button>
                </Card>
            </div>
      );
    }
}