# Relational Database Schema

## Notes
 - Last Updated 10/10/23
 - Many classes in the dataset have `TBA` for unknown meeting times, `TBD` for unknown profs

## Data-Containing Tables (User-Inaccessible)
`pathData(code char(10) NOT NULL, title varchar(200), crn char(5) NOT NULL, meets varchar(20), professor varchar(50), start_date char(10) NOT NULL, deleted int default 0, primary key(crn))`
 - This table has the same schema as the .csv data scraped from PATH
 - All data will be inserted into this table, then other tables populated from custom queries of this table
 - After all population has been done, this table will be unnecessary and should be able to be deleted
 - `code`, `crn`, and `start_date` are all primary keys in other tables

## Past Course Tables (User-Unmodifiable)

`course(course_id char(10) NOT NULL, title varchar(200), deleted int default 0, primary key(course_id))`
 - `course_id` is a 2/3/4-letter major code, a space, and a 5 digit number, e.g. "CSE 30246"

`section(crn char(5) NOT NULL, sem char(4) NOT NULL, course_id char(10), prof varchar(50), meets varchar(20), deleted int default 0, primary key(crn, sem))`
 - Section days and times `meets`, e.g. "TTh 3:30-4:45p"
 - 4-letter semester code `sem`, e.g. "FA23"

`sectionBelongsCourse(crn char(5) NOT NULL, sem char(4) NOT NULL, course_id char(10) NOT NULL, deleted int default 0, primary key(crn, sem))`

`courseHasPrereq(course_id char(10) NOT NULL, prereq_id char(10) NOT NULL, deleted int default 0, primary key(course_id, prereq_id))`

`courseHasCoreq(course_id char(10) NOT NULL, coreq_id char(10) NOT NULL, deleted int default 0, primary key(course_id, coreq_id))`

`major(major_code char(4) NOT NULL, deleted int default 0, primary key(major_code))`
 - 2/3/4-letter `major_code` from PATH, e.g. "EG", "CSE", "ACMS"
 - I can make a doc with all possible major codes if needed

`coreReq(req_code char(4) NOT NULL, deleted int default 0, primary key(req_code))`
 - 4-letter `req_code` codes from PATH, e.g. "WRRH" for writing & rhetoric
 - I can also compile all of these if needed
 - Also planning to use this for any requirement fulfilled by many courses, e.g. CSE electives

`majorRequiresCourse(major_code char(4) NOT NULL, course_id char(10) NOT NULL, deleted int default 0, primary key(major_code, course_id))`
 - For courses that are *explicitly* required by a major
 - i.e. CSE explicitly requires Discrete, but not Databases

`majorRequiresCoreReq(major_code char(4) NOT NULL, req_code char(5) NOT NULL, deleted int default 0, primary key(major_code, req_code))`

`courseFulfillsCoreReq(req_code char(5) NOT NULL, course_id char(10) NOT NULL, deleted int default 0, primary key(req_code, course_id))`

## Future Planning Tables (User-Modifiable)

`student(netid char(8) NOT NULL, name varchar(50) NOT NULL, major_code char(4), int gradyear, deleted int default 0, primary key(netid))`

`hasEnrollment(netid char(8) NOT NULL, course_id char(10) NOT NULL, sem char(4) NOT NULL, deleted int default 0, primary key(netid, course_id, sem))`
