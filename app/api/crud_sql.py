from sqlite3 import Row
from typing import List

from api import con
from types import DegreeType, JobType, Industry


def create_user(skills: List[str] = None) -> int:
    if skills is not None:
        skills = ','.join(skills)
    return con.execute('INSERT INTO user (skills) VALUES (?)', (skills,)) \
              .lastrowid


def read_user(id: int) -> Row:
    return con.execute('SELECT * FROM user WHERE id = ?', (id,)) \
              .fetchone()


def update_user(userID: int, new_skills: List[str]) -> bool:
    if new_skills is not None:
        new_skills = ','.join(new_skills)
    n = con.execute('UPDATE user SET skills = :skills WHERE id = :id',
                    {"id": userID, "skills": new_skills}).rowcount
    return n > 0


def delete_user(id: int) -> bool:
    n = con.execute('DELETE FROM user WHERE id = ?', (id,)).rowcount
    return n > 0


def create_university(name: str) -> Row:
    name = name.strip().title()  # Convert name to titlecase for consistency
    con.execute('INSERT INTO university VALUES (?)', (name,))
    return read_university(name)


def read_university(name: str) -> Row:
    # `name` column is `COLLATE NOCASE` so we just need to strip whitespace
    name = name.strip()
    return con.execute('SELECT * FROM university WHERE name = ?', (name,)) \
              .fetchone()


def update_university(old_name: str, new_name: str) -> bool:
    """Change the name of a university and update all references to it."""
    pass


def delete_university(name: str) -> bool:
    name = name.strip()
    n = con.execute('DELETE FROM university WHERE name = ?', (name,)).rowcount
    return n > 0


def create_course(name: str, num: str, uni: str) -> int:
    # standardize course name and number before inserting
    name = name.strip().title()
    num = num.strip().upper()

    university = read_university(uni)
    if university is None:
        create_university(uni)

    return con.execute('''INSERT INTO course (universityName, courseTitle, courseNumber)
                       VALUES (?, ?, ?)''', (uni, name, num)) \
              .lastrowid


def read_course(id: int) -> Row:
    return con.execute('SELECT * FROM course WHERE id = ?', (id,)) \
              .fetchone()


def find_course(name: str, num: str, uni: str) -> Row:
    name = name.strip()
    num = num.strip()
    uni = uni.strip()
    result = con.execute('''SELECT * FROM course
                            WHERE universityName = ?
                            AND courseTitle = ?
                            AND courseNumber = ?''',
                         (uni, name, num)) \
                .fetchone()
    if result is not None:
        return result

    result = con.execute('''SELECT * FROM course
                            WHERE universityName = ?
                            AND courseNumber = ?''',
                         (uni, num)) \
                .fetchone()

    if result is not None:
        return result

    result = con.execute('''SELECT * FROM course
                            WHERE universityName = ?
                            AND courseTitle = ?''',
                         (uni, name)) \
                .fetchone()
    return result  # may be None, but that's ok if none of the cases match


def update_course(id: int, **kwargs) -> bool:
    """Change the name/number of a course and update all references to it."""
    pass


def delete_course(id: int) -> bool:
    n = con.execute('DELETE FROM course WHERE id = ?', (id,)).rowcount
    return n > 0


def create_employer(name: str) -> Row:
    name = name.strip()
    c = con.execute('INSERT INTO employer (name) VALUES (?)', (name,))
    return c.execute('SELECT * FROM employer WHERE name = ?', (name,)) \
            .fetchone()


def read_employer(name: str) -> Row:
    name = name.strip()
    return con.execute('SELECT * FROM employer WHERE name = ?', (name,)) \
              .fetchone()


def update_employer(old_name: str, new_name: str) -> bool:
    """Change the name of an employer and update all references to it."""
    pass


def delete_employer(name: str) -> bool:
    name = name.strip()
    n = con.execute('DELETE FROM employer WHERE name = ?', (name,)).rowcount
    return n > 0


def create_position(employer: str, title: str) -> int:
    title = title.strip().title()
    emp = read_employer(employer)
    if emp is None:
        emp = create_employer(employer)

    return con.execute('''INSERT INTO position (employerName, jobTitle)
                          VALUES (?, ?)''', (emp['name'], title)) \
              .lastrowid


def read_position(id: int) -> Row:
    return con.execute('SELECT * FROM position WHERE id = ?', (id,)) \
              .fetchone()


def find_position(employer: str, title: str) -> Row:
    employer = employer.strip()
    title = title.strip()
    return con.execute('''SELECT * FROM position
                          WHERE employerName = ?
                          AND jobTitle = ?''',
                       (employer, title)) \
              .fetchone()


def update_position(id: int, **kwargs) -> bool:
    new_employer = kwargs.get('employer')
    new_title = kwargs.get('title')
    if new_employer:
        new_employer = 'employerName = ' + new_employer
    if new_title:
        new_title = 'title = ' + new_title

    set_clause = ', '.join((new_employer, new_title))
    if set_clause == '':
        return False
    n = con.execute('''UPDATE position
                       SET ?
                       WHERE id = ?''',
                    (set_clause, id)) \
           .rowcount
    return n > 0


def delete_position(id: int) -> bool:
    n = con.execute('DELETE FROM position WHERE id = ?', (id,)).rowcount
    return n > 0


def create_graduation(
    userID: int,
    uni: str,
    year: int,
    degree: DegreeType = None,
    major: str = None,
    gpa: float = None,
):
    university = read_university(uni)
    if university is None:
        university = create_university(uni)

    columns = ['userID', 'university', 'year']
    values = [userID, university['name'], year]
    if degree:
        columns.append('degree')
        values.append(degree.value())
    if major:
        columns.append('major')
        values.append(major)
    if gpa:
        columns.append('gpa')
        values.append(gpa)

    con.execute('INSERT INTO graduate (:columns) VALUES (:values)',
                {'columns': ', '.join(columns), 'values': ', '.join(values)})


def read_graduation(userID: int, uni: str, year: int) -> Row:
    uni = uni.strip()
    return con.execute('''SELECT * FROM graduate
                          WHERE userID = ?
                          AND university = ?
                          AND year = ?''',
                       (userID, uni, year)) \
              .fetchone()


def update_graduation(userID: int, uni: str, year: int, **kwargs) -> bool:
    uni = uni.strip()
    new_degree = kwargs['degree']
    new_major = kwargs['major']
    new_gpa = kwargs['gpa']

    if new_degree:
        new_degree = 'degree = ' + new_degree
    if new_major:
        new_major = 'major = ' + new_major
    if new_gpa:
        new_gpa = 'gpa = ' + new_gpa
    set_clause = ', '.join((new_degree, new_major, new_gpa))
    if set_clause == '':
        return False
    n = con.execute(''' UPDATE graduate
                        SET :set_clause
                        WHERE userID = :user
                        AND university = :uni
                        AND year = :year
                    ''',
                    {
                        'set_clause': set_clause,
                        'user': userID,
                        'uni': uni,
                        'year': year,
                    }) \
           .rowcount
    return n > 0


def delete_graduation(userID: int, uni: str, year: int) -> bool:
    uni = uni.strip()
    n = con.execute('''DELETE FROM graduate
                       WHERE userID = ?
                       AND university = ?
                       AND year = ?''',
                    (userID, uni, year)) \
           .rowcount
    return n > 0


def create_experience(
    userID: int,
    posID: int,
    industry: Industry = None,
    salary: int = None,
    type: JobType = None,
    rating: int = None,
):
    columns = ['userID', 'positionID']
    values = [userID, posID]
    if industry:
        columns.append('industry')
        values.append(industry.value())
    if salary:
        columns.append('salary')
        values.append(salary)
    if type:
        columns.append('type')
        values.append(type.value())
    if rating:
        columns.append('rating')
        values.append(rating)

    con.execute('INSERT INTO experience (:columns) VALUES (:values)',
                {'columns': ', '.join(columns), 'values': ', '.join(values)})


def read_experience(userID: int, posID: int) -> Row:
    return con.execute('''SELECT FROM experience
                          WHERE userID = ? AND positionID = ?''',
                       (userID, posID)) \
              .fetchone()


def update_experience(userID: int, posID: int, **kwargs) -> bool:
    new_industry = kwargs['industry']
    new_salary = kwargs['salary']
    new_type = kwargs['type']
    new_rating = kwargs['rating']

    if new_industry:
        new_industry = 'industry = ' + new_industry.value()
    if new_salary:
        new_salary = 'salary = ' + new_salary
    if new_type:
        new_type = 'type = ' + new_type.value()
    if new_rating:
        new_rating = 'rating = ' + new_rating
    set_clause = ', '.join((new_industry, new_salary, new_type, new_rating))
    if set_clause == '':
        return False
    n = con.execute('''UPDATE experience
                       SET :set_clause
                       WHERE userID = :user
                       AND positionID = :pos''',
                    {'set_clause': set_clause, 'user': userID, 'pos': posID}) \
           .rowcount
    return n > 0


def delete_experience(userID: int, posID: int) -> bool:
    n = con.execute('''DELETE FROM experience
                       WHERE userID = ? AND positionID = ?''',
                    (userID, posID)) \
           .rowcount
    return n > 0


def add_enrollment(userID: int, courseID: int) -> bool:
    n = con.execute('INSERT INTO enrollment VALUES (?, ?)', (userID, courseID)) \
           .rowcount
    return n > 0


def remove_enrollment(userID: int, courseID: int) -> bool:
    n = con.execute('''DELETE FROM enrollment
                       WHERE userID = ? AND courseID = ?''',
                    (userID, courseID)).rowcount
    return n > 0


# Explicit transaction management
def begin_transaction():
    con.execute('BEGIN')


def commit():
    con.commit()


def rollback():
    con.rollback()
