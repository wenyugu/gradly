import sys
import traceback
from flask import abort
from sqlite3 import Row
from typing import Any, Dict, List, Tuple, Union

import crud_sql as crud
import util

from api import app, con
from db_types import DegreeType, JobType, Industry

#take a user’s university 
#return a list of job titles that other users with similar education have reported
def get_job_for_education_background(education: str):
    return con.execute('SELECT p.jobTitle FROM graduate g NATURAL JOIN experience e, position p WHERE g.university = ? and e.PositionID = p.id', (education,)) \
              .fetchall()    
#take a desired job title + industry
#return a list of courses that people who have that (or similar) job took
def get_job_for_education_background(job: str, industry: str):
    return con.execute('SELECT c.courseTitle FROM experience eee NATURAL JOIN enrollment ee NATURAL JOIN experience e, position p, course c WHERE e.PositionID = p.id and p.jobTitle = ? and c.id = ee.courseID and eee.industry = ?', (job, industry,)) \
              .fetchall()    