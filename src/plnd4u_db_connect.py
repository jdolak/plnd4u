#!/usr/bin/env python3

import os
import mysql.connector
from dotenv import load_dotenv
import logging
import threading
import time
from retry import retry

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG = logging.getLogger()

load_dotenv()
DB_PASSWD = os.getenv('MYSQL_ROOT_PASSWORD')
DEPLOY_ENV = os.getenv('DEPLOY_ENV')

if DEPLOY_ENV == 'prod':
    FLASK_DEBUG = False
else:
    if not DEPLOY_ENV:
        DEPLOY_ENV = 'dev'
    FLASK_DEBUG = True



@retry(delay=0.5, backoff=2)
def _db_establish_connection():
    global DB
    global FLASK_DEBUG
    cwd = os.getenv('PWD')
    if cwd == "/plnd4u" or cwd == None:
        DB = mysql.connector.connect(
            host="plnd4u-db-1",
            port="3306",
            user="root",
            password=DB_PASSWD,
            database="plnd4u",
            auth_plugin='mysql_native_password'
        )
        db_keep_alive_thread = threading.Thread(target=_db_keep_alive, args=(7200,), daemon=True)
        db_keep_alive_thread.start()
    else:
        DB = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password=DB_PASSWD,
            database="plnd4u",
            auth_plugin='mysql_native_password'
        )

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