# Relational Database Schema

## Notes TBD
 - Incomplete: Last Updated 10/04/23
 - Re-determine keys for each relation
 - Can we force people to select pre-existing major codes?
   - Use a dropdown selector?
 - Is the major relation needed? Don't think so
 - Could coreReq be rewritten as an attribute for course?
   - Think deletion error

## Past Course Tables (User-Unmodifiable)

course(_course_id char(10)_, title varchar(50))
 - 'course_id' is a 2/3/4-letter major code, a space, and a 5 digit number, e.g. "CSE 30246"

section(_crn char(5)_, _sem char(4)_, course_id char(10), prof varchar(50), days char(5), time varchar(20))
 - 4-letter semester code 'sem', e.g. "FA23"

sectionBelongsCourse(_crn char(5)_, _sem char(4)_, _course_id char(10)_)

courseHasPrereq(_course_id char(10)_, prereq_id char(10))

courseHasCoreq(_course_id char(10)_, coreq_id char(10))

major(_major_code char(4)_)
 - 2/3/4-letter major codes from PATH, e.g. "EG", "CSE", "ACMS"
 - I can make a doc with all possible major codes if needed

coreReq(_req_code char(5)_)
 - 4/5-letter core requirement codes from PATH, e.g. "WRRH" for writing & rhetoric
 - I can also compile all of these if needed
 - Also planning to use this for any requirement fulfilled by many courses, e.g. CSE electives

majorRequiresCourse(_major_code char(4)_, _course_id char(10)_)
 - For courses that are *explicitly* required by a major
 - i.e. CSE explicitly requires Discrete, but not Databases

majorRequiresCoreReq(_major_code char(4)_, _req_code char(5)_)

courseFulfillsCoreReq(_req_code char(5)_, _course_id char(10)_)

## Future Planning Tables (User-Modifiable)

student(_netid char(8)_, name varchar(50), major_code char(4), int gradyear)

hasEnrollment(_netid char(8)_, _course_id char(10)_, _sem char(4)_)
