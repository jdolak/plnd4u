#!/usr/bin/env python3

from plnd4u_db_connect import *

# internal - don't use in prod
def db_show(limit):
    mycursor = DB.cursor()
    sql = "SELECT * FROM path_data LIMIT %s"
    val =  (limit, )
    mycursor.execute(sql,val)
    return list(mycursor)

def db_check_class_in_enrollment(netid, course_id, sem, title):
    mycursor = DB.cursor()

    sql = "SELECT enrollment_id, deleted FROM has_enrollment WHERE netid = %s AND course_id = %s AND sem = %s AND title = %s"
    val = (netid, course_id, sem, title)
    try:
        mycursor.execute(sql, val)
        result = list(mycursor)
    except Exception as e:
        LOG.error(e)
        return e

    return(result)

def db_enroll_class(netid, course_id, sem, title):
    mycursor = DB.cursor()

    sql = "INSERT INTO has_enrollment (enrollment_id, netid, course_id, sem, title) SELECT COUNT(*), %s, %s, %s, %s FROM has_enrollment"
    val = (netid, course_id, sem, title)
    try:
        mycursor.execute(sql, val)
        DB.commit()
        LOG.info(f"Class Enrolled : {netid} - {course_id} - {sem} - {title}")
        return 1
    except Exception as e:
        LOG.error(e)
        return e

def db_register_student(netid, name, major_code, gradyear):
    mycursor = DB.cursor()

    sql = "INSERT INTO student (netid, name, major_code, gradyear) VALUES (%s, %s, %s, %s)"
    val = (netid, name, major_code, gradyear)
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except:
        return 1
    
def db_search_past_classes(search, level):
    mycursor = DB.cursor()
    search = f"%{search}%"
    sql = "SELECT course_id, title FROM course WHERE deleted <> 1 AND (title LIKE %s or course_id LIKE %s)"
    val = (search, search)

    try:
        mycursor.execute(sql, val)
        results = list(mycursor)

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
    
def db_show_student_enrollments(netid):
    mycursor = DB.cursor()
    sql = "SELECT enrollment_id, course_id, sem, title, user_created FROM has_enrollment WHERE netid = %s AND deleted <> 1"
    val = (netid, ) 
    try:
        mycursor.execute(sql, val)
        return list(mycursor)
    except:
        return 1