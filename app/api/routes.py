from flask import request, abort
import sqlite3

import crud_sql as crud
import util
from api import app
from db_types import DegreeType, JobType, Industry

@app.route('/api/user/new', endpoint='new_user', methods=['POST'])
@app.route('/api/user/<int:userID>', endpoint='exisiting_user', methods=['GET', 'POST', 'DELETE'])
def user(userID=None):
    """Dispatch method for user operations.
    Calls the appropriate endpoint function based on the request method.
    """
    if request.endpoint == 'new_user':
        app.logger.info('Creating new user')
        return new_user(request.json)

    if request.method == 'GET':
        app.logger.info('Fetching user {}'.format(userID))
        return get_user(userID)
    elif request.method == 'POST':
        app.logger.info('Updating user {}'.format(userID))
        return update_user(userID, request.json)
    elif request.method == 'DELETE':
        app.logger.warn('Deleting user {}'.format(userID))
        return delete_user(userID)
    abort(405)


def new_user(request_json):
    """Endpoint for creating a new user.

    All information related to the user is provided in a JSON document. Missing
    values will be stored as null.

    The JSON schema is defined in `/api/schema.json`. The `delete` parameter is
    ignored, as is `id` (since we don't have an id yet).

    The newly created user's id is returned in a JSON object `{"userID": id}`.
    ---
    consumes:
      - application/json
    produces:
      - application/json
    responses:
        200:
            description: User created
        500:
            description: Exception occurred
    """
    app.logger.debug(request_json)
    skills = request_json.get('skills')
    education_history = request_json.get('education', [])
    work_history = request_json.get('experience', [])

    # Start an explicit transaction to avoid creating entities if later
    # operations fail.  The transaction will be rolled back upon exception.
    util.tx_begin()
    try:
        # create the user entity
        userID = crud.create_user(skills)

        # create education info
        for item in education_history:
            school = item['school']  # required field
            grad_date = item['year']  # required field
            degree = DegreeType(item.get('degree'))
            major = item.get('major')
            gpa = item.get('gpa')

            university = crud.read_or_create_university(school)
            crud.create_graduation(userID, university['name'], grad_date, degree, major, gpa)

            courses = item.get('courses', [])
            for c in courses:
                courseTitle = c['name']  # required field
                courseNumber = c['num']  # required field

                course = crud.find_course(courseTitle, courseNumber, university['name'])
                if course is not None:
                    courseID = course['id']
                else:
                    courseID = crud.create_course(courseTitle, courseNumber, university['name'])

                crud.add_enrollment(userID, courseID)

        # create work experience info
        for item in work_history:
            employerName = item['employer']   # required field
            title = item['title']  # required field
            industry = Industry(item.get('industry'))
            salary = item.get('salary')
            jobtype = JobType(item.get('type'))
            rating = item.get('rating')

            employer = crud.read_or_create_employer(employerName)
            position = crud.find_position(employerName, title)
            if position is not None:
                positionID = position['id']
            else:
                positionID = crud.create_position(employerName, title)

            crud.create_experience(userID, positionID, industry, salary, jobtype, rating)

        util.tx_commit()
        return {'userID': userID}
    # In the case of an exception, rollback any changes we made and report
    except Exception as e:
        util.tx_rollback()
        util.log_error(e)
        abort(500, e)


def get_user(userID):
    """Endpoint for retrieving information about a user.

    All information related to the specified user is returned in a JSON document
    describing each entry. Empty values will be returned as `null`.

    The document returned here is fully compatable with `new_user` and `update/user`
    endpoints. Updating a user with the JSON document returned here will result
    in a no-op, and creating a new user after deleting the current will restore
    the same values (potentially with a new userID though).
    ---
    produces:
      - application/json
    parameters:
      - name: userID
        in: path
        type: integer
        required: true
    responses:
        200:
            description: User found
        404:
            description: User not found
    """
    user = crud.read_user(userID)
    if user is None:
        abort(404, 'User {} does not exist.'.format(userID))

    userInfo = {'id': userID}

    skills = user['skills']
    if skills is not None:
        skills = skills.split(',')
    userInfo['skills'] = skills

    # TODO: high-level relation models (courses, graduated, etc) need to be implemented (probably as db functions)
    # courses = user.courses
    #
    # userInfo['education'] = []
    # for graduation in user.graduated:
    #     grad = {}
    #     grad['school'] = graduation.university
    #     grad['degree'] = graduation.degree.value
    #     grad['year'] = graduation.gradDate
    #     grad['major'] = graduation.major
    #     if graduation.gpa is not None:
    #         grad['gpa'] = float(graduation.gpa)
    #     else:
    #         grad['gpa'] = None
    #
    #
    #     grad['courses'] = []
    #     for course in courses:
    #         if course.universityName == graduation.university:
    #             grad['courses'].append({
    #                 'name': course.courseTitle,
    #                 'num': course.courseNumber,
    #             })
    #
    #     userInfo['education'].append(grad)
    #
    # userInfo['experience'] = []
    # for job in user.experience:
    #     positionID = job.positionID
    #     position = crud.read_position(positionID)
    #
    #     exp = {}
    #     exp['employer'] = position.employerName
    #     exp['title'] = position.jobTitle
    #     exp['industry'] = job.industry.value
    #     exp['salary'] = job.salary
    #     exp['type'] = job.type.value
    #     exp['rating'] = job.rating
    #
    #     userInfo['experience'].append(exp)

    return userInfo


def update_user(userID, request_json):
    """Endpoint for updating information of an existing user.

    The message body must contain a JSON document similar to that of a new user,
    however, only the fields which should be updated must be included. Any field
    which is present in the message body will be updated in the database, except
    primary keys.

    To delete an object, specify the keys necessary to identify it with the
    `delete` parameter set to `true`. The `skills` array is the exception to
    this, requiring an empty array `[]` instead (a `null` or missing value will
    be interpreted as "no change").
    ---
    consumes:
      - application/json
    parameters:
      - name: userID
        in: path
        type: integer
        required: true
    responses:
        200:
            description: User updated
        404:
            description: User not found
        500:
            description: Exception occured
    """
    skills = request_json.get('skills')
    education_history = request_json.get('education', [])
    work_history = request_json.get('experience', [])

    user = crud.read_user(userID)
    if user is None:
        abort(404, 'User {} does not exist.'.format(userID))

    util.tx_begin()
    try:
        # Only update skills if new skills are provided. If an empty list is given,
        # clear the user.skills attribute by setting skills to None.
        if skills is not None:
            if len(skills) == 0:
                skills = None
            crud.update_user(userID, skills)

        for item in education_history:
            school = item['school']  # required field
            grad_date = item['year']  # required field
            delete = item.get('delete', False)

            if delete:
                crud.delete_graduation(userID, school, grad_date)
                continue

            # NOTE: `item.get(key)`` will return `None` if the key is not present
            # which is distinct from a null value. Thus, we must only include the
            # argument if the key was actually present (even if `value` is `None`)
            kwargs = {}
            for key in ['degree', 'major', 'gpa']:
                if key in item:
                    value = item[key]
                    if key == 'degree':
                        value = DegreeType(value)
                    if key == 'gpa':
                        value = float(value)
                    kwargs[key] = value
            crud.update_graduation(userID, school, grad_date, **kwargs)

            courses = item.get('courses', [])
            for c in courses:
                courseTitle = c['name']  # required field
                courseNumber = c['num']  # required field
                delete = c.get('delete', False)

                course = crud.find_course(courseTitle, courseNumber, school)
                app.logger.info('Found course: {}'.format(dict(course)))

                if delete and course is not None:
                    app.logger.info('Removing course enrollment: {}'.format(course['courseNumber']))
                    crud.remove_enrollment(userID, course['id'])
                    continue

                if course is not None:
                    crud.update_course(course['id'], name=courseTitle, num=courseNumber)
                    courseID = course['id']
                else:
                    courseID = crud.create_course(courseTitle, courseNumber, school)

                crud.add_enrollment(userID, courseID)

        for item in work_history:
            employerName = item['employer']  # required field
            title = item['title']  # required field
            delete = item.get('delete', False)

            position = crud.find_position(employerName, title)

            if delete and position is not None:
                crud.delete_experience(userID, position['id'])
                continue

            if position is None:
                positionID = crud.create_position(employerName, title)
            else:
                positionID = position['id']

            # If the experience does not yet exist, create it,
            # otherwise update only those fields which appear in the data
            if crud.read_experience(userID, positionID) is None:
                industry = Industry(item.get('industry'))
                salary = item.get('salary')
                jobtype = JobType(item.get('type'))
                rating = item.get('rating')
                crud.create_experience(userID, positionID, industry, salary, jobtype, rating)
            else:
                kwargs = {}
                for key in ['industry', 'salary', 'type', 'rating']:
                    if key in item:
                        value = item[key]
                        if key == 'industry':
                            value = Industry(value)
                        elif key == 'type':
                            value = JobType(value)
                        kwargs[key] = value
                crud.update_experience(userID, positionID, **kwargs)

        # Return HTTP code 204 No Content to indicate success without a return value
        util.tx_commit()
        return ('', 204)
    except Exception as e:
        util.tx_rollback()
        util.log_error(e)
        abort(500, e)


def delete_user(userID):
    """Endpoint for removing a user and associated relationships.

    Completely remove a user. Any relationships relying on the userID as a
    primary key will also be deleted.
    ---
    parameters:
      - name: userID
        in: path
        type: integer
        required: true
    responses:
        200:
            description: User deleted
        404:
            description: User not found
    """
    user = crud.read_user(userID)
    if user is None:
        abort(404, 'User {} does not exist'.format(userID))

    crud.delete_user(userID)
    return {'status': 'Deleted user {}'.format(userID)}
