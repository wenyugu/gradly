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
    indicator than just anyone with a bachelors degree).
    """

    # Raises a 404 if the user is not found. That is exactly what we want
    _ = get_user(userID)

    # Alright, this is a bit complicated. We have two primary queries here: A
    # and B.
    #
    # Query B is easy, it just gets the User and Degree information of the user
    # we want to look up from the education table.
    #
    # Query A is harder. We start with education for the same info as B. Then
    # we join with experience to gain access to the postionID column, which we
    # then use to join with position, which gives us jobTitle and employerName.
    # We filter this by users that still exist in the table (in case a user was
    # deleted without removing their experience). Since this query does not
    # depend on variables, we can store it as a view to simplify the full query.
    #
    # Next, we join A and B on the condition that the userID is different,
    # essentially getting a cross product of our user with the work experience
    # of every other (current) user.
    #
    # We then group by the job info and aggregate using our custom weight
    # function which takes the education info of our user and the other user
    # to determine a relationship factor. We exclude the groups (jobs) which
    # have no relationship.
    #
    # Finally, we select the job title and employer name concatenated together
    # and the custom weight value and sort by descending weight.

    # NOTE: to change this view, the old version must first be DROP'ed
    # as views are read-only in SQLite
    con.execute('''CREATE VIEW IF NOT EXISTS all_jobs
                   (jobTitle, employerName, userID, university, degree, major)
                   AS
                   SELECT jobTitle, employerName, userID, university, degree, major
                   FROM (education NATURAL JOIN experience) e
                   JOIN position p
                   ON e.positionID = p.id
                   WHERE userID in (SELECT id FROM user)
                ''')

    rows = con.execute(
        '''
        SELECT jobTitle || ', ' || employerName as job,
        CAREER_WEIGHT(
            a.major, a.university, a.degree, b.major, b.university, b.degree
        ) as weight
        FROM all_jobs a
        JOIN
        (
            SELECT userID, university, degree, major
            FROM education
            WHERE userID = ?
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
    return {'status': 'OK', 'results': results}


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

    query = '''SELECT courseNumber || ': ' || courseTitle as course,
                      universityName as university
               FROM (experience NATURAL JOIN education) ex
               JOIN enrollment e
               ON e.educationID = ex.id
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
        results[row['university']][row['course']] += 1

    # for each university (key k), sort the list of courses by relevance
    for k, v in results.items():
        results[k] = list(map(lambda e: e[0],
                              sorted(v.items(),
                                     key=lambda x: x[1],
                                     reverse=True)
                             ))

    return results


def get_popular_companies(school: str, limit: int):
    rows = con.execute('''SELECT employerName, COUNT(userID) as cnt
                          FROM position p JOIN experience ex
                          ON p.id = ex.positionID
                          NATURAL JOIN education
                          WHERE university = ?
                          GROUP BY employerName
                          ORDER BY cnt DESC
                          LIMIT ?
                       ''', (school, limit)) \
              .fetchall()
    results = list(map(lambda x: x['employerName'], rows))
    return {'status': 'OK', 'results': results}
