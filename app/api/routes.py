import time
from flask import request

from api import app
# from api import db
# from models import *
import crud
from models import DegreeType, JobType, Industry


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


# @app.route('/api/db/commit')
# def commit():
#     db.session.commit()
#     return {'status': 'success'}
#
#
# @app.route('/api/db/rollback')
# def rollback():
#     db.session.rollback()
#     return {'status': 'success'}


@app.route('/api/new_user', methods=['POST'])
def new_user():
    skills = None
    education_history = []
    work_history = []
    print(request.json, flush=True)
    for key, value in request.json.items():
        if key == 'skills':
            skills = value
        elif key == 'education':
            education_history = value
        elif key == 'experience':
            work_history = value

    # create the user entity
    userID = crud.create_user(skills)

    # create education info
    for item in education_history:
        university = crud.read_or_create_university(item['school'])
        grad_date = item['year']
        if not isinstance(grad_date, int):
            raise TypeError
        degree = DegreeType(item['degree'])
        major = item['major']
        gpa = item['gpa']

        crud.create_graduation(userID, university.name, grad_date, degree, major, gpa)

        courses = item['courses']
        for c in courses:
            courseTitle = c['name']
            courseNumber = c['num']

            course = crud.find_course(courseTitle, courseNumber, university.name)
            if course is not None:
                courseID = course.id
            else:
                courseID = crud.create_course(courseTitle, courseNumber, university.name)

            crud.add_enrollment(userID, courseID)

    # create work experience info
    for item in work_history:
        employer = crud.read_or_create_employer(item['employer'])
        title = item['title']
        industry = Industry(item['industry'])
        print(industry, flush=True)
        salary = item['salary']
        jobtype = JobType(item['type'])
        rating = item['rating']

        position = crud.find_position(employer, title)
        if position is not None:
            positionID = position.id
        else:
            positionID = crud.create_position(employer, title)

        crud.create_experience(userID, positionID, industry, salary, jobtype, rating)

    return {'userID': userID}


@app.route('/api/user/<int:userID>')
def get_user(userID):
    user = crud.read_user(userID)

    userInfo = {}
    userInfo['skills'] = user.skills.split(',')

    courses = user.courses

    userInfo['education'] = []
    for graduation in user.graduated:
        grad = {}
        grad['school'] = graduation.university
        grad['degree'] = graduation.degree.value
        grad['year'] = graduation.gradDate
        grad['major'] = graduation.major
        grad['gpa'] = float(graduation.gpa)

        grad['courses'] = []
        for course in courses:
            if course.universityName == graduation.university:
                grad['courses'].append({
                    'name': course.courseTitle,
                    'num': course.courseNumber,
                })

        userInfo['education'].append(grad)

    userInfo['experience'] = []
    for job in user.experience:
        positionID = job.positionID
        position = crud.read_position(positionID)

        exp = {}
        exp['employer'] = position.employerName
        exp['title'] = position.jobTitle
        exp['industry'] = job.industry.value
        exp['salary'] = job.salary
        exp['type'] = job.type.value
        exp['rating'] = job.rating

        userInfo['experience'].append(exp)

    return userInfo


@app.route('/api/delete_user/<int:userID>')
def delete_user(userID):
    user = crud.read_user(userID)
    if user is not None:
        crud.delete_user(userID)
        return {'status': 'Deleted user {}'.format(userID)}
    return {'status': 'User {} does not exist'.format(userID)}
