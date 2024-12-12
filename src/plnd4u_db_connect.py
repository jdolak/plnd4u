#!/usr/bin/env python3

import os
import mysql.connector
import logging
import threading
import time
from retry import retry 
from sqlalchemy import create_engine, text, MetaData, and_, func
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.ext.automap import automap_base

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s() - %(message)s')
LOG = logging.getLogger()

DB_PASSWD = os.getenv('MYSQL_ROOT_PASSWORD')
DEPLOY_ENV = os.getenv('DEPLOY_ENV')
PORT = os.getenv('PORT')
DB_PROVIDER = os.getenv('DB_PROVIDER')
PEPPER = os.getenv('PEPPER')

if not PORT:
    PORT = 80

if DEPLOY_ENV == 'dev':
    FLASK_DEBUG = True
else:
    if not DEPLOY_ENV:
        DEPLOY_ENV = 'prod'
    FLASK_DEBUG = False

if not DB_PROVIDER in ('mysql', 'sqlite'):
    DB_PROVIDER = 'sqlite'

if not PEPPER:
    PEPPER = 'cGVwcGVyCg'

if not DB_PASSWD:
    PEPPER = 'root'


@retry(delay=0.5, backoff=2)
def _db_establish_connection():
    global DB
    global FLASK_DEBUG
    global LOCATION
    global ENGINE
    global Base
    global metadata
    cwd = os.getenv('PWD')
    #if False:
    if cwd == "/plnd4u" or cwd == None:
       # DB = mysql.connector.connect(
       #     host="plnd4u-db-1",
       #     port="3306",
       #     user="root",
       #     password=DB_PASSWD,
       #     database="plnd4u",
       #     auth_plugin='mysql_native_password',
       #     ssl_disabled= True
       # )
        host = 'plnd4u-db-1'

        #db_keep_alive_thread = threading.Thread(target=_db_keep_alive, args=(7200,), daemon=True).start()

        LOCATION = "container"
    else:
       # DB = mysql.connector.connect(
       #     host="localhost",
       #     port="3306",
       #     user="root",
       #     password=DB_PASSWD,
       #     database="plnd4u",
       #     auth_plugin='mysql_native_password'
       # )
       # host = 'localhost' 
        LOCATION = "local"

    if DB_PROVIDER == 'mysql':
        ENGINE = create_engine(f"mysql+pymysql://root:{DB_PASSWD}@{host}:3306/plnd4u", echo=True)
    else:
        ENGINE = create_engine("sqlite:///data/sqlite/data.db")

    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=ENGINE)

def _db_keep_alive(length):
    while True:
        try:
            mycursor = DB.cursor()
            sql = "SELECT NOW()"
            mycursor.execute(sql)
            LOG.info(f"Keep alive success: {list(mycursor)}")
        except Exception as e:
            LOG.error(f"Keepalive failed: {e}")

        time.sleep(length)

_db_establish_connection()

class Course(Base):
    __table__ = metadata.tables['course']

class CourseFulfillsCoreReq(Base):
    __table__ = metadata.tables['course_fulfills_core_req']

class CourseHasCoreq(Base):
    __table__ = metadata.tables['course_has_coreq']

class CourseHasPrereq(Base):
    __table__ = metadata.tables['course_has_prereq']

class Description(Base):
    __table__ = metadata.tables['description']

class HasEnrollment(Base):
    __table__ = metadata.tables['has_enrollment']

class Login(Base):
    __table__ = metadata.tables['login']

class Major(Base):
    __table__ = metadata.tables['major']

class MajorRequiresCourse(Base):
    __table__ = metadata.tables['major_requires_course']

class MajorRequiresElective(Base):
    __table__ = metadata.tables['major_requires_elective']

class Section(Base):
    __table__ = metadata.tables['section']

class Student(Base):
    __table__ = metadata.tables['student']


# pyright: reportMissingModuleSource=false