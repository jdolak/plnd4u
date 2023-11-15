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
    :returns: 1 on login failure, 0 on login success"""
    
    # obtain salt and hash from DB if they exist
    mycursor = DB.cursor()

    sql = "SELECT salt, hash FROM login WHERE netid = %s"
    val = (netid,)
    try:
        mycursor.execute(sql, val)
        result = list(mycursor)
    except Exception as e:
        LOG.error(e)
        return 1

    # fail if netid not in login table
    if len(result) == 0:
        LOG.error("Password check, password has no length")
        return 1
    
    # if salt hash pair found, convert to bytes
    salt_bytes = bytes.fromhex(result[0][0])
    hash_correct = bytes.fromhex(result[0][1])

    # hash the password attempt and compare
    try:
        password_attempt_bytes = password_attempt.encode()
    except UnicodeError as e:
        # invalid password
        LOG.error(f"Password check : {e}")
        return 1
    
    h = hashlib.new("sha256")
    h.update(password_attempt_bytes)
    h.update(salt_bytes)
    hash_attempt = h.digest()

    if not compare_digest(hash_attempt, hash_correct):
        # invalid match
        LOG.info("Password invalid match")
        return 1

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
    :returns: list of required courses unfulfilled in enrollments"""
    pass

def db_check_core_requirements(netid):
    """Cross-references a student's core requirements with their enrollments
    :returns: list of required core reqs unfulfilled in enrollments"""
    pass

# Advanced Function: Validate Requisite Reuirements

def db_check_course_conflicts(netid, enrollment_id):
    """Cross-references an enrollment's coreqs and prereqs with
    the student's other enrollments
    :returns: false if there exist needed coreqs or prereqs not in has_enrollments"""
    pass