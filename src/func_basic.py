#!/usr/bin/env python3

from plnd4u_db_connect import *

def db_show(limit):
    mycursor = DB.cursor()
    sql = "SELECT * FROM path_data LIMIT %s"
    val =  (limit, )
    mycursor.execute(sql,val)
    return list(mycursor)

def db_enroll_class(netid, course_id, sem):
    mycursor = DB.cursor()

    sql = "INSERT INTO has_enrollment (netid, course_id, sem) VALUES (%s, %s, %s)"
    val = (netid, course_id, sem)
    try:
        mycursor.execute(sql, val)
        DB.commit()
        LOG.info(f"Class Enrolled : {netid} - {course_id} - {sem}")
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
    
def db_search_past_classes(search):
    mycursor = DB.cursor()
    search = f"%{search}%"
    sql = "SELECT * FROM path_data WHERE title LIKE %s or code LIKE %s or crn LIKE %s AND deleted <> 1"
    val = (search, search, search)
    mycursor.execute(sql, val) 
    results = list(mycursor)

    if not len(results):
        return 0
    else:
        return results

def db_del_enrollment(netid, course_id, sem):
    mycursor = DB.cursor()
    sql = "UPDATE has_enrollment SET deleted = 1 WHERE netid = %s AND course_id = %s AND sem = %s"
    val = (netid, course_id, sem)
    try:
        mycursor.execute(sql, val)
        DB.commit()
        return 0
    except:
        return 1

def db_del_enrollment_permanent(netid, course_id, sem):
    mycursor = DB.cursor()
    sql = "DELETE FROM has_enrollment WHERE netid = %s AND course_id = %s AND sem = %s"
    val = (netid, course_id, sem)
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
    sql = "SELECT course_id, sem FROM has_enrollment WHERE netid = %s AND deleted <> 1"
    val = (netid, ) 
    try:
        mycursor.execute(sql, val)
        return list(mycursor)
    except:
        return 1