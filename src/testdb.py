#!/usr/bin/env python3

from plnd4u_db_connect import *

from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
Base.prepare(ENGINE, reflect=True)

YourTable = Base.classes.student

def main():

    session = Session(ENGINE)  
    mapped_tables = Base.classes
    print("Mapped Tables:")
    for table_name in mapped_tables:
        print(table_name)  # Prints table names


    # Example: Query a specific table
    YourTable = mapped_tables.student  # Replace with the actual table name
    results = session.query(YourTable).all()
    for row in results:
        print(row.name)
      

if __name__ == '__main__':
    main()