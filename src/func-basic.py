#!/usr/bin/env python3

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
DB_PASSWD = os.getenv('MYSQL_ROOT_PASSWORD')

db = mysql.connector.connect(
    host="localhost",
    port="9123",
    user="root",
    password=DB_PASSWD,
    database="plnd4u"
)

def db_show(limit):
    mycursor = db.cursor()
    mycursor.execute(f"SELECT * FROM path_data LIMIT {limit};")
    return list(mycursor)

def db_enroll_class(netid, course_id, sem):
    mycursor = db.cursor()

    sql = "INSERT INTO has_enrollment (netid, course_id, sem) VALUES (%s, %s, %s)"
    val = (netid, course_id, sem)
    
    try:
        mycursor.execute(sql, val)
        db.commit()
        return 0
    except:
        return 1

def db_register_student(netid, name, major_code, gradyear):
    mycursor = db.cursor()

    sql = "INSERT INTO student (netid, name, major_code, gradyear) VALUES (%s, %s, %s, %s)"
    val = (netid, name, major_code, gradyear)

    try:
        mycursor.execute(sql, val)
        db.commit()
        return 0
    except:
        return 1
    
def db_search_past_classes(search):
    mycursor = db.cursor()
    search = f"%{search}%"
    sql = "SELECT * FROM path_data WHERE title LIKE %s or code LIKE %s or crn LIKE %s"
    val = (search, search, search)
    mycursor.execute(sql, val) 
    results = list(mycursor)

    if not len(results):
        return 0
    else:
        return results

def db_del_enrollment():
    pass