# Relational Database Schema

## Notes TBD
 - Last Updated 10/10/23

## Past Course Tables (User-Unmodifiable)

`course(course_id char(10) NOT NULL, title varchar(200), deleted int default 0, primary key(course_id))`
 - 'course_id' is a 2/3/4-letter major code, a space, and a 5 digit number, e.g. "CSE 30246"

`section(crn char(5) NOT NULL, sem char(4) NOT NULL, course_id char(10), prof varchar(50), meets varchar(20), deleted int default 0, primary key(crn, sem))`
 - Section days and times 'meets', e.g. "TTh 3:30-4:45p"
 - 4-letter semester code 'sem', e.g. "FA23"

`sectionBelongsCourse(crn char(5) NOT NULL, sem char(4) NOT NULL, course_id char(10) NOT NULL, deleted int default 0, primary key(crn, sem))`

`courseHasPrereq(course_id char(10) NOT NULL, prereq_id char(10) NOT NULL, deleted int default 0, primary key(course_id, prereq_id))`

`courseHasCoreq(course_id char(10) NOT NULL, coreq_id char(10) NOT NULL, deleted int default 0, primary key(course_id, coreq_id))`

`major(major_code char(4) NOT NULL, deleted int default 0, primary key(major_code))`
 - 2/3/4-letter major codes from PATH, e.g. "EG", "CSE", "ACMS"
 - I can make a doc with all possible major codes if needed

`coreReq(req_code char(4) NOT NULL, deleted int default 0, primary key(req_code))`
 - 4-letter core requirement codes from PATH, e.g. "WRRH" for writing & rhetoric
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
