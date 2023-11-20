#!/usr/bin/env python3

from plnd4u_db_connect import *

def db_enroll_class(netid, course_id, sem, title):
    # check if enrollment exists
    if(len(db_check_class_in_enrollment(netid, course_id, sem, title, 0))):
        return 1

    # check if enrollment exists but has been deleted
    already_deleted_list = db_check_class_in_enrollment(netid, course_id, sem, title, 1)
    if(len(already_deleted_list)):
        enrollment_id = already_deleted_list[0][0]
        return db_undel_enrollment(enrollment_id)

    # if not, create the enrollment
    return db_create_enrollment(netid, course_id, sem, title)


def db_check_class_in_enrollment(netid, course_id, sem, title, deleted):
    mycursor = DB.cursor()

    sql = "SELECT enrollment_id FROM has_enrollment WHERE netid = %s AND course_id = %s AND sem = %s AND title = %s AND deleted = %s"
    val = (netid, course_id, sem, title, deleted)
    try:
        mycursor.execute(sql, val)
        result = list(mycursor)
    except Exception as e:
        LOG.error(e)
        return e

    return(result)


def db_create_enrollment(netid, course_id, sem, title):
    mycursor = DB.cursor()

    sql = "INSERT INTO has_enrollment (enrollment_id, netid, course_id, sem, title) SELECT COUNT(*), %s, %s, %s, %s FROM has_enrollment"
    val = (netid, course_id, sem, title)
    try:
        mycursor.execute(sql, val)
        DB.commit()
        LOG.info(f"Class Enrolled : {netid} - {course_id} - {sem} - {title}")
        return 0
    except Exception as e:
        LOG.error(e)
        return e

def db_undel_enrollment(enrollment_id):
    mycursor = DB.cursor()
    sql = "UPDATE has_enrollment SET deleted = 0 WHERE enrollment_id = %s"
    val = (enrollment_id, )
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except:
        return 1
    

def db_register_student(netid, name, major_code, gradyear):
    mycursor = DB.cursor()

    sql = "INSERT INTO student (netid, name, major_code, gradyear) VALUES (%s, %s, %s, %s)"
    val = (netid, name, major_code, gradyear)
    try:
        mycursor.execute(sql, val)
        DB.commit()
        LOG.info(f"Student Registered : {netid}")
        return 0
    except Exception as e:
        LOG.error(e)
        return 1
    
    
def db_search_past_classes(search, filters):
    mycursor = DB.cursor()
    search = f"%{search}%"

    levels = ""
    suffix = ""

    fall_semester   = filters[0] 
    spring_semester = filters[1] 
    level_one       = filters[2]
    level_two       = filters[3]
    level_three     = filters[4]
    level_four      = filters[5]
    uni_req         = filters[6]
    major_req       = filters[7]
    major_elective  = filters[8]

    if fall_semester:
        suffix = suffix
    if spring_semester:
        suffix = suffix
    if level_one:
        levels = levels + " OR course_id LIKE '%1____'"
    if level_two:
        levels = levels + " OR course_id LIKE '%2____'"
    if level_three:
        levels = levels + " OR course_id LIKE '%3____'"
    if level_four:
        levels = levels + " OR course_id LIKE '%4____'"
    """
    if uni_req:
        suffix = f""
    if major_req:
        suffix = f""
    if major_elective:
        suffix = f""
    """

    sql = f"SELECT course_id, title FROM course WHERE deleted <> 1 AND (title LIKE %s or course_id LIKE %s) AND (0=1{levels})"
    val = (search, search)

    try:
        # list comprehension to shorten course titles to max 80 chars
        # jachob dared me to do it
        mycursor.execute(sql, val)
        results = [tuple([row[i] if (i != 1 or len(str(row[i])) <= 80) else f'{row[1][:77]}...' for i in range(len(row))]) for row in list(mycursor)]

        LOG.info(sql)
        LOG.info(f"Class searched : {search}")
        if not len(results):
            return 0
        else:
            return results
        
    except Exception as e:
        LOG.error(e)
        return e


def db_del_enrollment(enrollment_id):
    mycursor = DB.cursor()
    sql = "UPDATE has_enrollment SET deleted = 1 WHERE enrollment_id = %s"
    val = (enrollment_id, )
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except:
        return 1
    

def db_del_enrollment_permanent(enrollment_id):
    mycursor = DB.cursor()
    sql = "DELETE FROM has_enrollment WHERE enrollment_id = %s"
    val = (enrollment_id, )
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except:
        return 1
    
    
def db_del_student(netid):
    mycursor = DB.cursor()
    sql = "UPDATE student SET deleted = 1 WHERE netid = %s"
    val = (netid, ) 
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except:
        return 1
    

def db_del_student_permanent(netid):
    mycursor = DB.cursor()
    sql = "DELETE FROM student WHERE netid = %s"
    val = (netid, )
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except:
        return 1
    
    
def db_update_student_major(netid, major_code):
    mycursor = DB.cursor()
    sql = "UPDATE student SET major_code = %s WHERE netid = %s"
    val = (major_code, netid) 
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except:
        return 1
    

def db_update_student_gradyear(netid, gradyear):
    mycursor = DB.cursor()
    sql = "UPDATE student SET gradyear = %s  WHERE netid = %s"
    val = (gradyear, netid) 
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except:
        return 1
    
    
def db_show_student_enrollments(netid, sem):
    mycursor = DB.cursor()
    sql = "SELECT enrollment_id, course_id, sem, title, user_created FROM has_enrollment WHERE netid = %s AND sem = %s AND deleted <> 1"
    val = (netid, sem) 
    try:
        mycursor.execute(sql, val)
        return list(mycursor)
    except:
        return 1


def db_show_student_enrollments_short(netid, sem):
    mycursor = DB.cursor()
    sql = "SELECT enrollment_id, course_id, sem, title, user_created FROM has_enrollment WHERE netid = %s AND sem = %s AND deleted <> 1"
    val = (netid, sem) 
    try:
        # list comprehension to shorten course titles to max 20 chars
        # jachob dared me to do it
        mycursor.execute(sql, val)
        return [tuple([row[i] if (i != 3 or len(str(row[i])) <= 20) else f'{row[3][:17]}...' for i in range(len(row))]) for row in list(mycursor)]
    except:
        return 1
    
    
def db_del_all_enrollments(netid):
    mycursor = DB.cursor()
    sql = "UPDATE has_enrollment SET deleted = 1 WHERE netid = %s"
    val = (netid, )
    try:
        mycursor.execute(sql, val)
        DB.commit()
        LOG.debug("Deleted all enrollments")
        return 0
    except:
        LOG.error("Did not delete all enrollments")
        return 1