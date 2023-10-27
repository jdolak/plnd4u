#!/usr/bin/env python3

import os
import mysql.connector
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG = logging.getLogger()

load_dotenv()
DB_PASSWD = os.getenv('MYSQL_ROOT_PASSWORD')

cwd = os.getenv('PWD')

if cwd == "/plnd4u" or cwd == None:
    DB = mysql.connector.connect(
        host="plnd4u-db-1",
        port="3306",
        user="root",
        password=DB_PASSWD,
        database="plnd4u"
    )
else:
    DB = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password=DB_PASSWD,
        database="plnd4u"
    )