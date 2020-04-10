import React, { Component } from 'react';
import './Profile.css';

const capitalize = (s) => {
    return s.charAt(0).toUpperCase() + s.slice(1)
}

export default class Profile extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        const { user } = this.props;
        return (
            <div id='resume'>
                {user ? (
                    <>
                    <dl>
                    <dt>Education</dt>
                    <dd>
                    {
                        user.education.map((el, idx) => (
                            <div key={`${el}~${idx}`}>
                                <h2>{el.school}</h2>
                                <p><strong>Degree </strong><span>{capitalize(el.degree)}</span></p>
                                <p><strong>Major </strong><span>{el.major}</span></p>
                                {el.gpa ? (<p><strong>GPA </strong><span>{el.gpa}</span></p>) : null}
                                <p><strong>Graduation Year </strong><span>{el.year}</span></p>
                                {<p><strong>Courses </strong></p>}
                                <ul>
                                {
                                    el.courses.map((course, index) => (
                                        <li key={index}>
                                            {course.num + "  " + course.name}
                                        </li>
                                    ))
                                }
                                </ul>
                            </div>
                        ))
                    }
                    </dd>
                </dl>
                <dl>
                    <dt>Experience</dt>
                    <dd>
                        {
                            user.experience.map((el, idx) => (
                                <div key={`${el}~${idx}`}>
                                    <h2>{el.employer}</h2>
                                    <p><strong>Title </strong><span>{el.title}</span></p>
                                    <p><strong>Employment Type </strong><span>{capitalize(el.type)}</span></p>
                                    <p><strong>Industry </strong><span>{el.industry}</span></p>
                                    {el.salary ? (<p><strong>Salary </strong><span>{el.salary}</span></p>) : null}
                                    {el.rating ? (<p><strong>Rating </strong><span>{el.rating}</span></p>) : null}
                                </div>
                            ))
                        }
                    </dd>
                </dl>
                <dl>
                    <dt>Skills</dt>
                    <dd>
                    {
                        user.skills.map((el, idx) => (
                            <div key={`${el}~${idx}`}>
                                <h2>{capitalize(el)}</h2>
                            </div>
                        ))
                    }
                    </dd>
                </dl>
                </>
                ) : null
                }
            </div>
        );
    }
}