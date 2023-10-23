# Relational Database Schema

## Notes
 - Implementing this schema on Azure as it is below
 - Last Updated 10/10/23
 - Many classes in the dataset have `TBA` for unknown meeting times, `TBD` for unknown profs
 - Data has ~100 instances of courses with same class code and different titles

## Data-Containing Tables (User-Inaccessible)
`path_data(code char(10) NOT NULL, title varchar(200), crn char(5) NOT NULL, meets varchar(75), professor varchar(50), start_date char(10) NOT NULL, deleted int default 0, primary key(crn))`
 - This table has the same schema as the .csv data scraped from PATH
 - All data will be inserted into this table, then other tables populated from custom queries of this table
 - After all population has been done, this table will be unnecessary and should be able to be deleted
 - `code`, `crn`, and `start_date` are all primary keys in other tables
 - `meets` has to be 75 characters due to oddly-formatted law research courses

`login(netid char(8) NOT NULL, salt varchar(100) NOT NULL, salted_hash varchar(100) NOT NULL)`

## Past Course Tables (User-Unmodifiable)

`course(course_id char(10) NOT NULL, title varchar(200), deleted int default 0, primary key(course_id))`
 - `course_id` is a 2/3/4-letter major code, a space, and a 5 digit number, e.g. "CSE 30246"

`section(crn char(5) NOT NULL, sem char(4) NOT NULL, course_id char(10), prof varchar(50), meets varchar(75), deleted int default 0, primary key(crn, sem))`
 - Section days and times `meets`, e.g. "TTh 3:30-4:45p"
 - 4-letter semester code `sem`, e.g. "FA23"

`course_has_prereq(course_id char(10) NOT NULL, prereq_id char(10) NOT NULL, deleted int default 0, primary key(course_id, prereq_id))`

`course_has_coreq(course_id char(10) NOT NULL, coreq_id char(10) NOT NULL, deleted int default 0, primary key(course_id, coreq_id))`

`major(major_code char(4) NOT NULL, deleted int default 0, primary key(major_code))`
 - 2/3/4-letter `major_code` from PATH, e.g. "EG", "CSE", "ACMS"
 - I can make a doc with all possible major codes if needed

`core_req(req_code char(4) NOT NULL, deleted int default 0, primary key(req_code))`
 - 4-letter `req_code` codes from PATH, e.g. "WRRH" for writing & rhetoric
 - I can also compile all of these if needed
 - Also planning to use this for any requirement fulfilled by many courses, e.g. CSE electives

`major_requires_course(major_code char(4) NOT NULL, course_id char(10) NOT NULL, deleted int default 0, primary key(major_code, course_id))`
 - For courses that are *explicitly* required by a major
 - i.e. CSE explicitly requires Discrete, but not Databases

`major_requires_core_req(major_code char(4) NOT NULL, req_code char(5) NOT NULL, deleted int default 0, primary key(major_code, req_code))`

`course_fulfills_core_req(req_code char(5) NOT NULL, course_id char(10) NOT NULL, deleted int default 0, primary key(req_code, course_id))`

## Future Planning Tables (User-Modifiable)

`student(netid char(8) NOT NULL, name varchar(50), major_code char(4), gradyear int, deleted int default 0, primary key(netid))`

`has_enrollment(netid char(8) NOT NULL, course_id char(10) NOT NULL, sem char(4) NOT NULL, deleted int default 0, primary key(netid, course_id, sem))`
