#!/usr/bin/env python3

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
DB_PASSWD = os.getenv('MYSQL_ROOT_PASSWORD')
DEPLOY_ENV = os.getenv('DEPLOY_ENV')

if DEPLOY_ENV == 'prod':
    FLASK_DEBUG = False
else:
    if not DEPLOY_ENV:
        DEPLOY_ENV = 'dev'
    FLASK_DEBUG = True

try:
    DB = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password=DB_PASSWD,
            database="plnd4u"
    )
except mysql.connector.errors.DatabaseError as e:
    print("Database not accessible, is it on?")
    exit(1)

def main():
    ans1 = input("This will delete all data from students and has_enrollment, permanently from your local db, proceed?: y/n ")
    if not (ans1 == 'y'):
        print("aborting...")              
        return 1
    
    if DEPLOY_ENV == 'prod':
        ans2 = input("This is this production database, are you sure?: y/n ")
        if not (ans2 == 'y'):
            print("aborting...")
            return 1
        
    mycursor = DB.cursor()
    sql = "DELETE FROM has_enrollment"

    try:
        mycursor.execute(sql)
        DB.commit()
        print("Deleted enrollment data")
    except Exception as e:
        print(e)
        return 1
    
    sql = "DELETE FROM student"
    
    try:
        mycursor.execute(sql)
        DB.commit()
        print("Deleted student data")
    except Exception as e:
        print(e)
        return 1
    
    return 0


if __name__ == '__main__':
    main()