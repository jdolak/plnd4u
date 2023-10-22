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

mycursor = db.cursor()

mycursor.execute("SELECT * FROM path_data LIMIT 20;")

for x in mycursor:
  print(x)