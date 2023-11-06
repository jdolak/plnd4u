#!/usr/bin/env python3

import hashlib
import secrets
from plnd4u_db_connect import *

# Advanced Function: Secure login

def db_create_login(netid, password):
    """Generates and inserts a salt and hash for a new user
    :returns: -1 on failure, 0 on success"""

    try:
        password_bytes = password.encode()
    except UnicodeError:
        # invalid password
        return -1
    
    # generate salt and salted hash
    salt_bytes = secrets.token_bytes(32)
    h = hashlib.new("sha256")
    h.update(password_bytes)
    h.update(salt_bytes)

    # TODO: store netid, hex strings of salt and hash in db
    print(netid)
    print(h.hexdigest())
    print(salt_bytes.hex())

def db_check_login(netid, password):
    """Checks if hash of login exists in database"""
    pass


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