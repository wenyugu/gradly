from flask import request, abort

from api import app
from logic.user import new_user, get_user, update_user, delete_user
from logic.function import get_job_for_education_background, get_classes_for_career


@app.route('/api/user/new', endpoint='new_user', methods=['POST'])
@app.route('/api/user/<int:userID>',
           endpoint='exisiting_user',
           methods=['GET', 'POST', 'DELETE'])
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


@app.route('/api/query/careers', endpoint='careers', methods=['GET'])
@app.route('/api/query/courses', endpoint='courses', methods=['GET'])
def query():
    args = request.args

    if request.endpoint == 'careers':
        user = args.get('userID')
        if user == None:
            abort(400, 'Please provide a userID ("careers?userID=<id>")')
        return get_job_for_education_background(user)
    else:  # endpoint == 'courses'
        university = args.get('university')
        industry = args.get('industry')
        title = args.get('title')
        return get_classes_for_career(industry, title, university)
