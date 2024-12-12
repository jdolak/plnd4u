#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import hashlib
from hmac import compare_digest
import secrets
from flask import g
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
    
    # generate salted hash
    load_dotenv()
    pepper_bytes = os.getenv('PEPPER').encode()
    salt_bytes = secrets.token_bytes(32)
    h = hashlib.new("sha256")
    h.update(password_bytes)
    h.update(salt_bytes)
    h.update(pepper_bytes)

    # store netid, hex strings of salt and hash in db
    #mycursor = DB.cursor()

    #sql = "INSERT INTO login(netid, salt, hash) VALUES (%s, %s, %s)"
    sql = text("INSERT INTO login(netid, salt, hash) VALUES (:netid, :salt, :hash)")
    #val = (netid, salt_bytes.hex(), h.hexdigest())
    try:
        result = g.db_session.execute(sql, {"netid": netid, "salt" : salt_bytes.hex(), "hash" : h.hexdigest()})
        #mycursor.execute(sql, val)
        #DB.commit()
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
    #mycursor = DB.cursor()

    #sql = "SELECT salt, hash FROM login WHERE netid = %s"
    sql = text("SELECT salt, hash FROM login WHERE netid = :netid")
    #val = (netid,)
    try:
        #mycursor.execute(sql, val)
        result = g.db_session.execute(sql, {"netid": netid})
        #result = g.db_session.query(Login.salt, Login.hash).filter(Login.netid == netid).all()
        result = list(result)
        LOG.info(f"login list : {result}")

    except Exception as e:
        LOG.error(e)
        return 2

    # fail if netid not in login table
    if len(result) == 0:
        LOG.error("Netid not in login table")
        return 3
    
    # if salt hash pair found, convert to bytes
    load_dotenv()
    pepper_bytes = os.getenv('PEPPER').encode()
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
    h.update(pepper_bytes)
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

    #sql = "SELECT course_id FROM major_requires_course WHERE course_id NOT IN (SELECT course_id FROM has_enrollment WHERE netid=%s AND deleted <> 1) AND major_code IN (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1) AND deleted <> 1"
    sql = text("SELECT course_id FROM major_requires_course WHERE course_id NOT IN (SELECT course_id FROM has_enrollment WHERE netid=:netid AND deleted <> 1) AND major_code IN (SELECT major_code FROM student WHERE netid=:netid AND deleted <> 1) AND deleted <> 1")
    #val = (netid, netid) 
    try:
        #mycursor = DB.cursor()
        #mycursor.execute(sql, val)
        result = g.db_session.execute(sql, {"netid": netid})
        missing_reqs = [i[0] for i in list(result)]
    except Exception as e:
        LOG.error(e)
        return "Error"
    
    if not len(missing_reqs):
        missing_reqs = "None"
        return missing_reqs
        
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
    
    #sql = "SELECT req_code FROM has_enrollment AS he, course_fulfills_core_req AS cfcr WHERE he.course_id = cfcr.course_id AND netid = %s AND he.deleted <> 1 AND cfcr.deleted <> 1"
    sql = text("SELECT req_code FROM has_enrollment AS he, course_fulfills_core_req AS cfcr WHERE he.course_id = cfcr.course_id AND netid = :netid AND he.deleted <> 1 AND cfcr.deleted <> 1")
    val = (netid, ) 
    try:
        #mycursor = DB.cursor()
        #mycursor.execute(sql, val)
        result = g.db_session.execute(sql, {"netid": netid})
        queried_reqs = [i[0] for i in list(result)]
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
    if not (fulfilled["WKIN"] or (fulfilled["WKAL"] and fulfilled["WKLC"]) or (fulfilled["WKHI"] and fulfilled["WKSS"])):
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
        missing_reqs = "None,"
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
    # sql = "SELECT he.course_id, mrc.elective_code FROM has_enrollment AS he, course_fulfills_core_req AS cfcr, major_requires_elective AS mrc, student AS s WHERE s.netid=%s AND s.major_code=mrc.major_code AND cfcr.req_code=mrc.elective_code AND cfcr.course_id=he.course_id AND he.deleted <> 1 AND s.deleted <> 1 ORDER BY mrc.priority DESC"
    sql = text("SELECT he.course_id, mrc.elective_code FROM has_enrollment AS he, course_fulfills_core_req AS cfcr, major_requires_elective AS mrc, student AS s WHERE s.netid=:netid AND s.major_code=mrc.major_code AND cfcr.req_code=mrc.elective_code AND cfcr.course_id=he.course_id AND he.deleted <> 1 AND s.deleted <> 1 ORDER BY mrc.priority DESC")
    #val = (netid, ) 
    try:
        #mycursor = DB.cursor()
        #mycursor.execute(sql, val)
        result = g.db_session.execute(sql, {"netid": netid})
        fulfilled_query = list(result)
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
    #sql = "SELECT elective_code, duplicate_count FROM major_requires_elective WHERE major_code IN (SELECT major_code FROM student WHERE netid=%s AND deleted <> 1) AND deleted <> 1"
    sql = text("SELECT elective_code, duplicate_count FROM major_requires_elective WHERE major_code IN (SELECT major_code FROM student WHERE netid=:netid AND deleted <> 1) AND deleted <> 1")
    #val = (netid, ) 
    try:
        #mycursor = DB.cursor()
        #mycursor.execute(sql, val)
        result = g.db_session.execute(sql, {"netid": netid})
        needed = {i[0] : i[1] for i in list(result)}
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
        output = "None,"
    return output[:-1]
    

# Advanced Function: Validate Requisite Reuirements

def db_check_corequisites(netid):
    """Cross-references an enrollment's coreqs and prereqs with
    the student's other enrollments
    :returns: false if there exist needed coreqs or prereqs not in has_enrollments"""

    missing = {}

    try:
        if True:
        #with DB.cursor() as mycursor:
            sql = text("""
            SELECT H.netid, H.course_id, R.coreq_id, H.sem, H.deleted
            FROM has_enrollment H, course_has_coreq R 
            WHERE netid = :netid AND H.course_id = R.course_id;
            """)
            #mycursor.execute(sql, (netid,))
            result = g.db_session.execute(sql, {"netid": netid})
            corequisites = [value for value in list(result) if value[-1] == 0]

            for _, code, coreq, sem, _ in corequisites:
                if sem == "UNLT":
                    continue
                
                #mycursor.execute("SELECT * from has_enrollment WHERE course_id = %s and sem = %s and deleted <> 1;", (coreq, sem))
                sql = text("SELECT * from has_enrollment WHERE course_id = :course_id and sem = :sem and deleted <> 1;")
                result = g.db_session(sql, {"course_id": coreq, "sem" : sem})
                cursor_list = list(result)
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

    semesters = ["UNLT", "FRFA", "FRSP", "SOFA", "SOSP", "JUFA", "JUSP", "SEFA", "SESP"]
    missing = {}

    try:
        if True:
        #with DB.cursor() as mycursor:
            sql = text("""
            SELECT H.netid, H.course_id, R.prereq_ids, H.sem 
            FROM has_enrollment H, course_has_prereq R 
            WHERE netid = :netid AND H.course_id = R.course_id;
            """)
            #mycursor.execute(sql, (netid,))
            result = g.db_session.execute(sql, {"netid": netid})
            prerequisites = list(result)

            for _, code, prereqs, sem in prerequisites:
                satisfied = False
                if sem == "UNLT":
                    continue

                for req in prereqs.split(","):
                    # mycursor.execute("SELECT sem from has_enrollment WHERE course_id = %s AND deleted <> 1;", (req,))
                    g.db_session.execute(text("SELECT sem from has_enrollment WHERE course_id = :req AND deleted <> 1;"), {"req": req})
                    semesters_taken = [sem[0] for sem in mycursor]
                    print(semesters_taken)

                    if semesters_taken and not(semesters.index(semesters_taken[0]) >= semesters.index(sem)):
                        satisfied = True
                if not satisfied:
                    missing.setdefault(code, []).append(prereqs.replace(",", " or "))

        return missing if missing else None

    except Exception as e:
        LOG.error(e)
        return 1
