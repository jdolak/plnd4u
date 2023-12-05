#!/usr/bin/env python3

import hashlib
from hmac import compare_digest
import secrets
from func_basic import *

# Advanced Function: Secure login

def db_create_login(netid, password):
    """Generates and inserts a salt and hash for a new user
    :returns: 1 on failure, 0 on success"""

    if len(password) == 0:
        # invalid password
        LOG.error(f"Invalid password, has no length: {password}")
        return 1

    try:
        password_bytes = password.encode()
    except UnicodeError as e:
        # invalid password
        LOG.error(f"Invalid password: {password} : {e}")
        return 1
    
    # generate salt and salted hash
    salt_bytes = secrets.token_bytes(32)
    h = hashlib.new("sha256")
    h.update(password_bytes)
    h.update(salt_bytes)

    # store netid, hex strings of salt and hash in db
    mycursor = DB.cursor()

    sql = "INSERT INTO login(netid, salt, hash) VALUES (%s, %s, %s)"
    val = (netid, salt_bytes.hex(), h.hexdigest())
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except Exception as e:
        LOG.error(f"Failed to create login : {e}")
        return 1

def db_check_login(netid, password_attempt):
    """Checks if hash of login exists in database
    RETURN VALUES
        0   login succes
        1   login failure
        2   error
        3   netid not matched
    """
    
    # obtain salt and hash from DB if they exist
    mycursor = DB.cursor()

    sql = "SELECT salt, hash FROM login WHERE netid = %s"
    val = (netid,)
    try:
        mycursor.execute(sql, val)
        result = list(mycursor)
    except Exception as e:
        LOG.error(e)
        return 2

    # fail if netid not in login table
    if len(result) == 0:
        LOG.error("Netid not in login table")
        return 3
    
    # if salt hash pair found, convert to bytes
    salt_bytes = bytes.fromhex(result[0][0])
    hash_correct = bytes.fromhex(result[0][1])

    # hash the password attempt and compare
    try:
        password_attempt_bytes = password_attempt.encode()
    except UnicodeError as e:
        # invalid password
        LOG.error(f"Password check : {e}")
        return 2
    
    h = hashlib.new("sha256")
    h.update(password_attempt_bytes)
    h.update(salt_bytes)
    hash_attempt = h.digest()

    if not compare_digest(hash_attempt, hash_correct):
        # invalid match
        LOG.info("Password invalid match")
        return 1

    LOG.info(f"Login success: logged in {netid}")
    return 0

def register_student(netid, name, major_code, gradyear, password):
    """
    Abstraction function that resisters a student by added them to the 
    student database and generates password hash

    RETURN VAULES:
        0   Success
        1   Student in database
        2   Password creation failed
    """
    if db_register_student(netid, name, major_code, gradyear):
        LOG.error("Failed to register student.")
        return 1
    if db_create_login(netid,password):
        LOG.error("Failed to create login.")
        return 2
    LOG.info(f"Student registration success: {netid}")
    return 0


# Advanced Function: Validate Major Requirements

def mike_ryan(netid):
    """Runs necessary functions to check if all major requirements 
    fulfilled (named by Prof. Weninger)
    :returns: list of unfulfilled courses and core reqs"""

def db_check_required_courses(netid):
    """Cross-references a student's major requirements with their enrollments

    RETURN VAULES:
        "None"      Success -- no requirements missing
        "Error"     Query error -- check all tables exist in database
        "c1,c2,..." Requirements missing
    """

    sql = "SELECT course_id FROM major_requires_course WHERE course_id NOT IN (SELECT course_id FROM has_enrollment WHERE netid=%s AND deleted <> 1) AND major_code IN (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1) AND deleted <> 1"
    val = (netid, netid) 
    try:
        mycursor = DB.cursor()
        mycursor.execute(sql, val)
        missing_reqs = [i[0] for i in list(mycursor)]
    except Exception as e:
        LOG.error(e)
        return "Error"
    
    if not len(missing_reqs):
        missing_reqs = "None"
        
    return ",".join(missing_reqs)

def db_check_core_requirements(netid):
    """Cross-references a student's core requirements with their enrollments

    RETURN VAULES:
        "None"      Success -- no requirement groups missing
        "Error"     Error obtaining enrolled courses
        "r1,r2,..." Requirement groups missing
    """

    core_reqs = {"WKAL", "WKCD", "WKDT", "WKFP", "WKFT", "WKHI", "WKIN", "WKLC", "WKQR", "WKSP", "WKSS", "WKST", "WRIT", "WRRH", "USEM", "FYS1", "FYS2"}
    fulfilled = {c : 0 for c in core_reqs}
    
    sql = "SELECT req_code FROM has_enrollment AS he, course_fulfills_core_req AS cfcr WHERE he.course_id = cfcr.course_id AND netid = %s AND he.deleted <> 1 AND cfcr.deleted <> 1"
    val = (netid, ) 
    try:
        mycursor = DB.cursor()
        mycursor.execute(sql, val)
        queried_reqs = [i[0] for i in list(mycursor)]
    except Exception as e:
        LOG.error(e)
        return "Error"
    
    for q in queried_reqs:
        if q in core_reqs:
            fulfilled[q] += 1

    missing_reqs = ""

    # Liberal Arts Requirements -- Six Ways of Knowing
    if not fulfilled["WKQR"]:
        missing_reqs = f'{missing_reqs}Liberal Arts 1 - Quantitative Reasoning,'
    if not fulfilled["WKST"]:
        missing_reqs = f'{missing_reqs}Liberal Arts 2 - Science & Technology,'
    if (fulfilled["WKQR"] < 2) and (fulfilled["WKST"] < 2):
        missing_reqs = f'{missing_reqs}Liberal Arts 3 - Quantitative Reasoning or Science & Technology,'
    if not (fulfilled["WKAL"] or fulfilled["WKLC"]):
        missing_reqs = f'{missing_reqs}Liberal Arts 4 - Art & Literature or Advanced Language & Culture,'
    if not (fulfilled["WKHI"] or fulfilled["WKSS"]):
        missing_reqs = f'{missing_reqs}Liberal Arts 5 - History or Social Science,'
    if (not fulfilled["WKIN"]) and ((fulfilled["WKAL"], fulfilled["WKLC"], fulfilled["WKHI"], fulfilled["WKSS"]).count(0) > 1):
        missing_reqs = f'{missing_reqs}Liberal Arts 6 - Integration or a Way of Knowing not already used in LA4 or LA5,'

    # Philo and Theo Requirements
    if not fulfilled["WKFP"]:
        missing_reqs = f'{missing_reqs}Introductory Philosophy,'
    if not (fulfilled["WKSP"] or fulfilled["WKCD"]):
        missing_reqs = f'{missing_reqs}Philosophy or Catholicism & the Disciplines,'
    if not fulfilled["WKFT"]:
       missing_reqs = f'{missing_reqs}Foundational Theology,'
    if not fulfilled["WKDT"]:
       missing_reqs = f'{missing_reqs}Developmental Theology,'

    # Writing Requirements
    if not fulfilled["USEM"]:
       missing_reqs = f'{missing_reqs}University Seminar,'
    if not fulfilled["WRIT"]:
       missing_reqs = f'{missing_reqs}Writing Intensive,'

    # Moreau
    if not fulfilled["FYS1"]:
       missing_reqs = f'{missing_reqs}Moreau First Year Experience Fall,'
    if not fulfilled["FYS2"]:
       missing_reqs = f'{missing_reqs}Moreau First Year Experience Spring,'

    if not len(missing_reqs):
        missing_reqs = "None"
    return missing_reqs[:-1]

def db_check_electives(netid):
    """Cross-references a student's elective requirements with their enrollments

    RETURN VAULES:
        "None"          Success -- no requirements missing
        "Error: ..."    Error obtaining enrollments that fulfill electives
        "Error: ..."    Error obtaining needed elective counts
        "e1,e2,..."     Requirements missing
    """

    # obtain the student's enrollments which fulfill needed electives
    # sql = "SELECT pe.course_id, pe.elective_code FROM (SELECT course_id, req_code AS elective_code FROM course_fulfills_core_req cfcr WHERE req_code IN (SELECT elective_code AS req_code FROM major_requires_elective WHERE major_code IN (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1))) pe, (SELECT course_id FROM has_enrollment WHERE netid=%s AND course_id NOT IN (SELECT course_id FROM major_requires_course WHERE major_code in (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1) AND deleted <> 1) and deleted <> 1) nr WHERE pe.course_id = nr.course_id ORDER BY pe.elective_code"
    # sql = "SELECT a.course_id, a.elective_code FROM (SELECT cfcr.course_id, req_code AS elective_code FROM course_fulfills_core_req cfcr, (SELECT course_id FROM has_enrollment WHERE netid=%s AND course_id NOT IN (SELECT course_id FROM major_requires_course WHERE major_code in (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1) AND deleted <> 1) and deleted <> 1) nr WHERE cfcr.course_id = nr.course_id AND cfcr.deleted <> 1) a, (SELECT course_id, req_code AS elective_code, priority FROM course_fulfills_core_req cfcr, (SELECT elective_code, priority FROM major_requires_elective WHERE major_code IN (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1)) pe WHERE cfcr.req_code=pe.elective_code) b WHERE a.course_id = b.course_id AND a.elective_code = b.elective_code ORDER BY priority DESC"
    sql = "SELECT enrollments.course_id, elective_code FROM (SELECT course_id, elective_code, priority FROM (SELECT * from major_requires_elective WHERE major_code IN (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1)) reqs, course_fulfills_core_req cfcr WHERE reqs.elective_code = cfcr.req_code AND course_id NOT IN (SELECT course_id FROM major_requires_course WHERE major_code IN (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1))) electives, (SELECT he.course_id, cfcr.req_code FROM has_enrollment he, course_fulfills_core_req cfcr WHERE he.course_id=cfcr.course_id) enrollments WHERE electives.course_id=enrollments.course_id and electives.elective_code=enrollments.req_code ORDER BY priority DESC"
    val = (netid, netid) 
    try:
        mycursor = DB.cursor()
        mycursor.execute(sql, val)
        fulfilled_query = list(mycursor)
    except Exception as e:
        LOG.error(e)
        return "Error: enrollments could not be obtained"
    
    fulfilled = {}
    for q in fulfilled_query:
        if q[0] not in fulfilled:
            fulfilled[q[0]] = [q[1]]
        else:
            fulfilled[q[0]].append(q[1])
    
    # obtain number of elective needed for major
    sql = "SELECT elective_code, duplicate_count FROM major_requires_elective WHERE major_code IN (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1) AND deleted <> 1"
    val = (netid, ) 
    try:
        mycursor = DB.cursor()
        mycursor.execute(sql, val)
        needed = {i[0] : i[1] for i in list(mycursor)}
    except Exception as e:
        LOG.error(e)
        return "Error: needed electives could not be obtained"
    
    for course in fulfilled:
        counted = False
        for e in fulfilled[course]:
            if counted:
                continue
            if (e in needed) and (needed[e] > 0):
                needed[e] -= 1
                counted = True

    output = ""
    for e in needed:
        if needed[e] > 0:
            output = f'{output}{needed[e]} {e} elective(s),'

    if not len(output):
        output = "None"
    return output[:-1]
    

# Advanced Function: Validate Requisite Reuirements

def db_check_corequisites(netid):
    """Cross-references an enrollment's coreqs and prereqs with
    the student's other enrollments
    :returns: false if there exist needed coreqs or prereqs not in has_enrollments"""

    missing = {}

    try:
        with DB.cursor() as mycursor:
            sql = """
            SELECT H.netid, H.course_id, R.coreq_id, H.sem, H.deleted
            FROM has_enrollment H, course_has_coreq R 
            WHERE netid = %s AND H.course_id = R.course_id;
            """
            mycursor.execute(sql, (netid,))
            corequisites = [value for value in list(mycursor) if value[-1] == 0]

            for _, code, coreq, sem, _ in corequisites:
                mycursor.execute("SELECT * from has_enrollment WHERE course_id = %s and sem = %s and deleted = 0;", (coreq, sem))

                cursor_list = list(mycursor)
                if not cursor_list:
                    missing.setdefault(code, []).append(coreq)

        return missing if missing else None

    except Exception as e:
        LOG.error(e)
        return 1


def db_check_prerequisites(netid):
    """Cross-references an enrollment's coreqs and prereqs with
    the student's other enrollments
    :returns: false if there exist needed coreqs or prereqs not in has_enrollments"""

    semesters = ["FRFA", "FRSP", "SOFA", "SOSP", "JUFA", "JUSP", "SEFA", "SESP"]
    missing = {}

    try:
        with DB.cursor() as mycursor:
            sql = """
            SELECT H.netid, H.course_id, R.prereq_ids, H.sem 
            FROM has_enrollment H, course_has_prereq R 
            WHERE netid = %s AND H.course_id = R.course_id;
            """
            mycursor.execute(sql, (netid,))
            prerequisites = list(mycursor)

            for _, code, prereqs, sem in prerequisites:
                for req in prereqs.split(","):
                    mycursor.execute("SELECT sem from has_enrollment WHERE course_id = %s AND deleted = 0;", (req,))
                    semesters_taken = [sem[0] for sem in mycursor]

                    if not semesters_taken or semesters.index(semesters_taken[0]) >= semesters.index(sem):
                        missing.setdefault(code, []).append(req)

        return missing if missing else None

    except Exception as e:
        LOG.error(e)
        return 1
