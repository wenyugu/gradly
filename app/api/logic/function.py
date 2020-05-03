from collections import defaultdict, OrderedDict
from flask import abort
from sqlite3 import Row
from typing import Any, Dict, List, Tuple, Union

import crud_sql as crud
import util

from api import app, con
from db_types import DegreeType, JobType, Industry
from logic.user import get_user

# take a user’s university
# return a list of job titles that other users with similar education have reported
def get_job_for_education_background(userID: int):
    """Get a list of jobs held by users of similar educational background.

    For each entry in this user's education, attempt to match other users
    by major, degree, and university. Major is required for a valid match,
    but degree and university may vary.

    For each match, the weight of the result is increased. Weights are computed
    in three dimensions: major matches, degree matches, and university matches.
    The results are ranked by the weighted average of these dimensions,
    with relative weights of 1, 2, 3 respectively (i.e. matches from the same
    university count more than just same major).
    """

    # Raises a 404 if the user is not found. That is exactly what we want
    userInfo = get_user(userID)

    response = {'status': 'OK',
                'results': [],
               }

    background = []
    for edu in userInfo['education']:
        uni = edu['school']
        degree = edu.get('degree')
        major = edu.get('major')
        background.append((uni, degree, major))

    if len(background) == 0:
        response['status'] = 'No education history found'
        return response

    results = defaultdict(lambda: [0,0,0])
    for uni, degree, major in background:
        # Major is not a required DB field, but this query is pretty meaningless
        # without knowing the major, so we will skip it
        if major is None:
            response['status'] = 'No major specified for at least one entry'
            continue

        # Get all positions where the user's major matches. Also return the
        # university and degree for later ranking
        rows = con.execute('''SELECT jobTitle, employerName, university, degree
                              FROM (graduation
                              NATURAL JOIN experience) e
                              JOIN position p
                              ON e.positionID = p.id
                              WHERE userID <> ?
                              AND major = ?
                           ''', (userID, major)) \
                  .fetchall()

        for row in rows:
            career = row['jobTitle'] + ', ' + row['employerName']
            # We know the major matches. This line also inserts the career if it
            # didn't already exist
            results[career][0] += 1

            if degree is not None and row['degree'] == degree:
                results[career][1] += 1

            if uni is not None and row['university'] == uni:
                results[career][2] += 1

    ranked_results = []
    for k, v in results.items():
        weight = (v[0] + 2 * v[1] + 3 * v[2]) / 6
        ranked_results.append((k, weight))

    response['results'] = sorted(ranked_results, key=lambda x: x[1], reverse=True)
    return response


# take a desired job title + industry
# return a list of courses that people who have that (or similar) job took
def get_classes_for_career(industry: str, job: str = None, university: str = None):
    """Return a list of potential classes related to the given industry.

    Classes are filtered by users who work in a particular position/industry
    who have reported taking those classes.

    If a specific job title is given, only users who have held that title are
    considered.

    A university name may be provided to restrict results to a particular
    university.

    Returns a dictionary mapping university names to a list of course numbers
    and titles, sorted aplhabetically
    """
    try:
        _ = Industry(industry).value
    except ValueError:
        abort(400, 'Invalid industry: {}'.format(industry))

    params = [industry]
    query_join_position = ''
    query_filter_title = ''
    query_filter_university = ''

    if job is not None:
        params.append(job)
        query_join_position = 'JOIN position p ON e.positionID = p.id'
        query_filter_title = 'AND jobTitle = ?'

    if university is not None:
        params.append(university)
        query_filter_university = 'AND university = ?'

    query = '''SELECT courseTitle, courseNumber, universityName as university
               FROM (experience NATURAL JOIN enrollment) e
               JOIN course c
               ON e.courseID = c.id
               {}
               WHERE industry = ?
               {}
               {}
            '''.format(query_join_position, query_filter_title, query_filter_university)

    rows = con.execute(query, params).fetchall()

    # build a dictionary mapping universities to courses
    # (deduplicating by using a set)
    results = defaultdict(set)
    for row in rows:
        course = row['courseNumber'] + ': ' + row['courseTitle']
        results[row['university']].add(course)

    # for each university (key k), sort the list of courses
    for k, v in results.items():
        results[k] = sorted(v)

    return results
