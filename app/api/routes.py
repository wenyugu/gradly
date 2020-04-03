import time
from flask import request

from api import app
from api import db
from models import *


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


@app.route('/api/user', methods=['GET', 'POST'])
def user():
    """Lookup (GET) or add (POST) a user.
    For lookups, the userID is provided as URL parameter 'id'.
    For new users, skills are provided as a string in the POST
    body with key 'skills'.
    """
    if request.method == 'POST':
        try:
            skills = request.form['skills']
        except KeyError:
            skills = None
        user = User(skills=skills)
        db.session.add(user)
        db.session.commit()
        return {'status': 'success', 'id': user.id}
    else:
        userID = request.args.get('id', '', type=int)
        user = User.query.get(userID)
        return {'id': user.id, 'skills': user.skills}


@app.route('/api/university', methods=['GET', 'POST'])
def university():
    """Lookup (GET) or add (POST) a university.
    Key (university name) is specified as URL parameter 'name'.
    """
    name = request.args.get('name', '')
    if request.method == 'POST':
        uni = University(name=name)
        db.session.add(uni)
        db.session.commit()
        return {'status': 'success', 'id': uni.name}
    else:
        uni = University.query.get(name)
        return {'name': uni.name}


@app.route('/api/course', methods=['GET', 'POST'])
def course():
    """Lookup (GET) or add (POST) a course.
    Lookups require course id ('id') and university name ('name') as URL parameters.
    Insertions require 'name', 'title', and optionally 'area' in the POST body.
    """
    if request.method == 'POST':
        name = request.form['name'] # TODO: do we have to enforce foreign key contraints?
        title = request.form['title']
        try:
            area = request.form['area']
        except KeyError:
            area = None
        course = Course(universityName=name, courseTitle=title, focusArea=area)
        db.session.add(course)
        db.session.commit()
        return {'status': 'success', 'id': course.id}
    else:
        id = request.args.get('id', '', type=int)
        name = request.args.get('name', '')
        course = Course.query.get(id=id, universityName=name)
        return {'id': course.id,
                'university': course.universityName,
                'title': course.courseTitle,
                'focusArea': course.focusArea,
                }
