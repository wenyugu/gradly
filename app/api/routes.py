from flask import request, abort

from api import app
from logic.user import new_user, get_user, update_user, delete_user
from logic.function import get_classes_for_career, \
                           get_job_for_education_background, \
                           get_popular_companies


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


@app.route('/api/query/careers', methods=['GET'])
def careers():
    """Endpoint to get relevant job recommendations based on user's background.

    Returns a JSON object with a status message ('OK' if everything is fine) and
    a list of jobs, sorted by relevance.
    """
    user = request.args.get('userID')
    if user == None:
        abort(400, 'Please provide a userID ("careers?userID=<id>")')
    return get_job_for_education_background(user)


@app.route('/api/query/courses', methods=['GET'])
def courses():
    """Endpoint to get relevant courses by career path.

    Industry of interest is passes as a query parameter. Industry names must
    match the standardized list of industries, with special characters (and
    whitespace) encoded using the standard HTML encoding sequences. Spaces may
    alternatively be replaced by '+'

    Optionally, the desired job title may be provided, following the same
    encoding scheme as above. A university name may also be specified to limit
    the results to a particular school.

    Returns a JSON object containing lists of courses keyed by the university
    which offers them.
    """
    args = request.args
    industry = args['industry']  # required
    title = args.get('title')
    university = args.get('university')
    return get_classes_for_career(industry, title, university)


@app.route('/api/query/popular_companies', methods=['GET'])
def popular_companies():
    uni = request.args['school']
    limit = request.args.get('limit') or 10
    return get_popular_companies(uni, limit)


# TODO: add endpoint to get list of all skills for use in form
