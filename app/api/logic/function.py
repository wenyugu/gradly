from collections import defaultdict, OrderedDict
from flask import abort
from sqlite3 import Row
from typing import Any, Dict, List, Tuple, Union

import crud_sql as crud
import util

from api import app, con
from db_types import DegreeType, JobType, Industry
from logic.user import get_user


class CareerWeight:
    def __init__(self):
        self.weight = 0

    def step(self, m1, u1, d1, m2, u2, d2):
        self.weight += 3 * (m1 == m2) + 2 * (u1 == u2) + (d1 == d2)

    def finalize(self):
        return self.weight


con.create_aggregate("CAREER_WEIGHT", 6, CareerWeight)


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
    with relative weights of 3, 1, 2 respectively (i.e. people in your major are
    better indicators than anyone at your university, which itself is a better
    indicator than anyone with a bachelors degree).
    """

    # Raises a 404 if the user is not found. That is exactly what we want
    userInfo = get_user(userID)

    response = {'status': 'OK',
                'results': [],
               }

    # Join `graduation`, `experience`, and `position` to get records for
    # every postion held by each user (other than the given one) with information
    # about each of the user's graduations. Thus, if user A graduated from S and R
    # and held jobs X and Y, then we will see rows such as
    #   A S X
    #   A S Y
    #   A R X
    #   A R Y
    # We are interested in the job (S and R above) as well as the degree to
    # which the user's education matches our own. We use a custom aggregate
    # function which takes the major, university, and degree type of two users
    # and outputs a number from 0 to 6, where 0 indicates no match and 6 is
    # a full match.
    # We exclude aggregated rows which have a zero sum, as they did not match
    # the user in any way. The final row returned includes the job (title
    # and employer) and the computed weight for this particular education set.
    rows = con.execute(
        '''
        SELECT jobTitle || ', ' || employerName as job,
        CAREER_WEIGHT(
            a.major, a.university, a.degree, b.major, b.university, b.degree
        ) as weight
        FROM
        (
            SELECT jobTitle, employerName, userID, university, degree, major
            FROM (graduation NATURAL JOIN experience) e
            JOIN position p
            ON e.positionID = p.id
            WHERE userID in (SELECT id FROM user)
        ) a
        JOIN
        (
            SELECT userID, university, degree, major
            FROM graduation
            WHERE userID = :uid
        ) b
        ON a.userID <> b.userID
        GROUP BY jobTitle, employerName
        HAVING CAREER_WEIGHT(
            a.major, a.university, a.degree, b.major, b.university, b.degree
        ) > 0
        ORDER BY weight DESC
        ''',
        (userID,)
    ).fetchall()

    results = [{'role': r['job'], 'relevance': r['weight']} for r in rows]
    response['results'] = results
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

    # build a dictionary mapping universities to courses, with each course having
    # an associate count (as a relevance metric)
    results = defaultdict(lambda: defaultdict(int))
    for row in rows:
        course = row['courseNumber'] + ': ' + row['courseTitle']
        results[row['university']][course] += 1

    # for each university (key k), sort the list of courses by relevance
    for k, v in results.items():
        results[k] = list(map(lambda e: e[0],
                              sorted(v.items(),
                                     key=lambda x: x[1],
                                     reverse=True)
                             ))

    return results
