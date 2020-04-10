import React, { Component, Fragment } from 'react';
import { Accordion, Alert, Button, Card, Form, Row, Col } from 'react-bootstrap';
import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';
import './DataEntry.css';
import { empOptions, degreeOptions, industryOptions, institutionOptions, skillsOptions, yearOptions } from '../../constants/options';
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import RangeSlider from 'react-bootstrap-range-slider';
import { defaultEducation, defaultExperience, defaultEducations, defaultExperiences } from '../../constants/constant';
const axios = require('axios');

const selectStyles = {
    menuPortal: base => ({ ...base, zIndex: 9999 }),
    menu: provided => ({ ...provided, zIndex: "9999 !important" })
};

const capitalize = (s) => {
    if (typeof s !== 'string') return s;
    return s.charAt(0).toUpperCase() + s.slice(1)
}

export default class DataEntry extends Component {
    constructor(props) {
        super(props);
        this.user = props.user;
        this.update = props.update;
        if (this.user) {
            this.state = this.user;
        } else {
            this.state = {
                education: defaultEducations,
                experience: defaultExperiences,
                skills: [],
                uid: 0,
                success: false
            };
        }
    }

    addEducation = () => {
        const values = [...this.state.education];
        values.push(defaultEducation);
        this.setState({education: values});
    }

    removeEducation = index => {
        const values = [...this.state.education];
        values.splice(index, 1);
        this.setState({ education: values });
    };

    addCourse = index => {
        const values = JSON.parse(JSON.stringify(this.state.education)); 
        values[index].courses.push({num: '', name: ''});
        this.setState({ education: values });
    };

    removeCourse = (num, index) => {
        const values = [...this.state.education];
        values[num].courses.splice(index, 1);
        this.setState({ education: values });
    }

    addExperience = () => {
        const values = [...this.state.experience];
        values.push(defaultExperience);
        this.setState({experience: values});
    }

    removeExperience = index => {
        const values = [...this.state.experience];
        values.splice(index, 1);
        this.setState({ experience: values });
    };

    handleEducationChange = (input, idx) => event => {
        const values = [...this.state.education];
        values[idx][input] = event.target.value;
        this.setState({
            education: values,
        });
    }

    handleExperienceChange = (input, idx) => event => {
        const values = [...this.state.experience];
        var value = event.target.value;
        if (input === 'rating' || input === 'salary') {
            value = parseInt(value);
        }
        values[idx][input] = value;
        this.setState({ 
            experience : values 
        });
    }

    handleCourseChange = (item, pidx, sidx) => event => {
        const values = [...this.state.education];
        values[pidx].courses[sidx][item] = event.target.value;
        this.setState({
            education: values,
        });
    }

    handleSkillsChange = options => {
        const values = options.map(el => (el.value));
        this.setState({ 
            skills : values 
        });
    }

    handleEducationSelect = (input, idx) => option => {
        if (!option) {return;}
        const values = [...this.state.education];
        values[idx][input] = option.value;
        this.setState({
            education: values,
        });
    }

    handleExperienceSelect = (input, idx) => option => {
        if (!option) {return;}
        const values = [...this.state.experience];
        values[idx][input] = option.value;
        this.setState({
            experience: values,
        });
    }

    handleSubmit = event => {
        const form = event.currentTarget;
        event.preventDefault();
        if (form.checkValidity() === false) {
            event.stopPropagation();
        } else {
            // validated
            const user = {
                education: this.state.education,
                experience: this.state.experience,
                skills: this.state.skills
            };
            if (this.update) {
                this.update(user);
            } else {
                axios.post('/api/user/new', user)
                    .then(response => {
                        this.setState({ uid: response.data.userID, success: true });
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        }
    }

    getOption = data => {
        if (Array.isArray(data)) {
            return data.map(el => ({ value: el, label: capitalize(el)}));
        }
        return { value: data, label: capitalize(data)};
    }

    render() {
        const { user, update } = this.props;
        return (
            <div>
                {
                    this.state.success ?
                        (<Alert variant="success">
                            <Alert.Heading>Submitted succesfully</Alert.Heading>
                            <p>
                                Thank you! We have received your response. Your userID is {this.state.uid}. Remember you can always update or delete your entry by using your ID.
                            </p>
                        </Alert>) :
                        (null)
                }

                <Form onSubmit={this.handleSubmit}>
                <Accordion defaultActiveKey="0" style={{textAlign: 'left'}}>
                    <Card>
                        <Accordion.Toggle as={Card.Header} variant="link" eventKey="0">
                            Education
                        </Accordion.Toggle>
                        <Accordion.Collapse eventKey="0">
                            <Card.Body>
                                    {
                                        this.state.education.map((el, idx) => (
                                            <Fragment key={`${el}~${idx}`}>
                                                <Button variant="dark" className='float-right' size='sm' onClick={() => this.removeEducation(idx)}>—</Button>
                                                <Form.Group>
                                                    <Form.Label style={{marginBottom: '18px'}}>School</Form.Label>
                                                    <CreatableSelect
                                                        isClearable
                                                        isSearchable
                                                        menuPortalTarget={document.querySelector('body')}
                                                        styles={selectStyles}
                                                        options={institutionOptions}
                                                        defaultValue={user ? this.getOption(user.education[idx].school) : null}
                                                        onChange={this.handleEducationSelect('school', idx)}
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
                                                        defaultValue={user ? this.getOption(user.education[idx].degree) : null}
                                                        onChange={this.handleEducationSelect('degree', idx)}
                                                    />
                                                </Form.Group>
                                                <Row>
                                                    <Col>
                                                        <Form.Group>
                                                            <Form.Label>Major</Form.Label>
                                                            <Form.Control 
                                                                placeholder="Major" 
                                                                type="text"
                                                                required
                                                                value={user ? user.education[idx].major: this.state.education[idx].major}
                                                                onChange={this.handleEducationChange('major', idx)}
                                                            />
                                                            <Form.Control.Feedback type="invalid">
                                                                Please enter your major.
                                                            </Form.Control.Feedback>
                                                        </Form.Group>
                                                    </Col>
                                                    <Col>
                                                        <Form.Group>
                                                            <Form.Label>GPA</Form.Label>
                                                            <Form.Control
                                                                placeholder="GPA: Optional"
                                                                type="number"
                                                                value={user ? user.education[idx].gpa : (this.state.education[idx].gpa || '')}
                                                                onChange={this.handleEducationChange('gpa', idx)}
                                                            />
                                                        </Form.Group>
                                                    </Col>
                                                </Row>
                                                <Form.Group >
                                                    <Form.Label>Graduation Year</Form.Label>
                                                    <Select
                                                        className="basic-single"
                                                        classNamePrefix="select"
                                                        isSearchable
                                                        menuPortalTarget={document.querySelector('body')}
                                                        styles={selectStyles}
                                                        options={yearOptions}
                                                        defaultValue={user ? this.getOption(user.education[idx].year) : null}
                                                        onChange={this.handleEducationSelect('year', idx)}
                                                    />
                                                </Form.Group>
                                                <Form.Label>Courses</Form.Label>
                                                {
                                                    this.state.education[idx].courses.map((elem, index) => (
                                                        <Fragment key={`${elem}~${index}`}>
                                                            <Button variant="dark" className='float-right' size='sm' onClick={() => this.removeCourse(idx, index)}>—</Button>
                                                            <Row>
                                                                <Col>
                                                                    <Form.Group>
                                                                        <Form.Label>Course Name</Form.Label>
                                                                        <Form.Control 
                                                                            placeholder="Ex. Database Systems" 
                                                                            type='text'
                                                                            value={user ? user.education[idx].courses[index].name : this.state.education[idx].courses[index].name}
                                                                            onChange={this.handleCourseChange('name', idx, index)}
                                                                        />
                                                                    </Form.Group>
                                                                </Col>
                                                                <Col>
                                                                    <Form.Group>
                                                                        <Form.Label>Course Number</Form.Label>
                                                                        <Form.Control 
                                                                            placeholder="Ex. CS411" 
                                                                            type='text'
                                                                            value={user ? user.education[idx].courses[index].num : this.state.education[idx].courses[index].num}
                                                                            onChange={this.handleCourseChange('num', idx, index)}
                                                                        />
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
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                    <Card>
                        <Accordion.Toggle as={Card.Header} variant="link" eventKey="2">
                            Experience
                        </Accordion.Toggle>
                        <Accordion.Collapse eventKey="2">
                            <Card.Body>
                                    {
                                        this.state.experience.map((el, idx) => (
                                            <Fragment key={`${el}~${idx}`}>
                                                <Button variant="dark" className='float-right' size='sm' onClick={() => this.removeExperience(idx)}>—</Button>
                                                <Form.Group>
                                                    <Form.Label>Employer</Form.Label>
                                                    <Form.Control 
                                                        placeholder="Ex. Google" 
                                                        type='text'
                                                        required
                                                        value={user ? user.experience[idx].employer : this.state.experience[idx].employer}
                                                        onChange={this.handleExperienceChange('employer', idx)}
                                                    />
                                                    <Form.Control.Feedback type="invalid">
                                                        Please enter your employer.
                                                    </Form.Control.Feedback>
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Title</Form.Label>
                                                    <Form.Control 
                                                        placeholder="Ex. Software Engineer" 
                                                        type='text'
                                                        required
                                                        value={user ? user.experience[idx].title : this.state.experience[idx].title}
                                                        onChange={this.handleExperienceChange('title', idx)}
                                                    />
                                                    <Form.Control.Feedback type="invalid">
                                                        Please enter your title.
                                                    </Form.Control.Feedback>
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
                                                        defaultValue={user ? this.getOption(user.experience[idx].type) : null}
                                                        onChange={this.handleExperienceSelect('type', idx)}
                                                    />
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Industry</Form.Label>
                                                    <CreatableSelect
                                                        isClearable
                                                        isSearchable
                                                        menuPortalTarget={document.querySelector('body')}
                                                        styles={selectStyles}
                                                        options={industryOptions}
                                                        defaultValue={user ? this.getOption(user.experience[idx].industry) : null}
                                                        onChange={this.handleExperienceSelect('industry', idx)}
                                                    />
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Annual Salary</Form.Label>
                                                    <Form.Control 
                                                        placeholder='USD per year'
                                                        type='number'
                                                        value={user ? this.state.experience[idx].salary : this.state.experience[idx].salary}
                                                        onChange={this.handleExperienceChange('salary', idx)}
                                                    />
                                                    <Form.Control.Feedback type="invalid">
                                                        Please enter your estimated salary.
                                                    </Form.Control.Feedback>
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Rating (0-10)</Form.Label>
                                                    <RangeSlider value={user ? this.state.experience[idx].rating : this.state.experience[idx].rating} onChange={this.handleExperienceChange('rating', idx)} max={10} />
                                                </Form.Group>
                                            </Fragment>
                                        ))
                                    }
                                    <div>
                                        <Button variant="primary" onClick={this.addExperience}>Add experience</Button>
                                    </div>
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                    <Card>
                        <Accordion.Toggle as={Card.Header} variant="link" eventKey="3">
                            Skills
                        </Accordion.Toggle>
                        <Accordion.Collapse eventKey="3">
                            <Card.Body>
                                    <Form.Group>
                                        <Form.Label>Skills</Form.Label>
                                        <CreatableSelect
                                            isMulti
                                            menuPortalTarget={document.querySelector('body')}
                                            styles={selectStyles}
                                            options={skillsOptions}
                                            defaultValue={user ? this.getOption(user.skills) : null}
                                            onChange={this.handleSkillsChange}
                                        />
                                    </Form.Group>
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                </Accordion>
                <Card>
                    <Button type='submit'>Submit</Button>
                </Card>
                </Form>
            </div>
      );
    }
}